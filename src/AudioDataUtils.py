import copy
import sys
import wave

import numpy as np # type: ignore
import pickle
import pyaudio # type: ignore
from scipy.io import wavfile # type: ignore
from typing import Tuple, Optional

BYTES_PER_SAMPLE = 2
AUDIO_WRITE_CHUNK_SIZE = 1024


"""A representation of audio data. Try to use this as if it were immutable."""
class AudioData:
    '''Sampling frequency in Hz. If these differ between two AudioData objects, overlaying one onto the other will
     involve upsampling or downsampling.'''
    sampling_freq: int

    '''An n by 1 numpy array where n is the length of the audio clip in seconds times the sampling frequency.
    Exactly one audio channel is assumed for simplicity. Each element in the array is a 32-bit float.'''
    time_amplitudes: np.ndarray

    def __init__(self, wav_filepath: Optional[str] = None,
                 pickled_filepath: Optional[str] = None,
                 manual_init: Tuple[int, np.ndarray] = None):
        if wav_filepath is not None:
            self.init_from_wav_filepath(wav_filepath=wav_filepath)
        elif pickled_filepath is not None:
            self.load(pickled_filepath)
        elif manual_init is not None:
            self.sampling_freq = manual_init[0]
            self.time_amplitudes = manual_init[1]
        else:
            raise ValueError("You must specify an argument to the AudioData constructor!")

    def init_from_wav_filepath(self, wav_filepath: str):
        assert_wav_file(wav_filepath)
        fs, data = wavfile.read(wav_filepath)
        self.sampling_freq = fs
        # Save only the audio from the first channel. Later, it might be useful to extract multiple channels.
        # This comes with the sizable assumption that the voice data is in the first channel. If this turns out to be
        # untrue, we can try to superimpose all of the channels on top of each other.
        if len(data.shape) == 1:
            self.time_amplitudes = data.astype(np.float32)
        else:
            self.time_amplitudes = data[:, 0].astype(np.float32)

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump((self.sampling_freq, self.time_amplitudes), file, -1)

    def load(self, filepath):
        with open(filepath, 'rb') as file:
            self.sampling_freq, self.time_amplitudes = pickle.load(file)


def play(audiodata: AudioData):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(BYTES_PER_SAMPLE),
                    channels=1, rate=audiodata.sampling_freq, output=True)
    try:
        num_samples = audiodata.time_amplitudes.shape[0]
        for i in range(0, num_samples//AUDIO_WRITE_CHUNK_SIZE + 1):
            left_bound = i*AUDIO_WRITE_CHUNK_SIZE
            right_bound = min(left_bound + AUDIO_WRITE_CHUNK_SIZE, num_samples)
            if left_bound == right_bound:
                break
            chunk = audiodata.time_amplitudes[left_bound:right_bound].astype(np.int16)
            stream.write(chunk.tobytes())
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def assert_wav_file(wav_filepath: str):
    with wave.open(wav_filepath, 'rb') as wf:
        bytes_per_sample = wf.getsampwidth()
        if bytes_per_sample != BYTES_PER_SAMPLE:
            raise ValueError("We only support files with" + str(8 * BYTES_PER_SAMPLE) + "-bit samples for now.")
        num_channels: int = wf.getnchannels()
        if num_channels > 1:
            print("WARNING: " + wav_filepath + " has " + str(num_channels) +
                  " audio channels, all but the first will be suppressed to simplify our model.", file=sys.stderr)


"""Returns a 3-tuple of AudioData objects: the combined audio, rescaled audio1, and rescaled audio2"""
def superimpose(audio_1: AudioData, audio_2: AudioData) -> Tuple[AudioData, AudioData, AudioData]:
    if audio_1.sampling_freq != audio_2.sampling_freq:
        # It is technically possible to upsample/downsample audio, but that can introduce losses that complicate our efforts.
        # For now, let's see if we can get all of our audio sources at a standard sampling frequency.
        raise ValueError("Superimposing 2 AudioData sources with different sampling frequencies is unsupported.")
    long_data = audio_1
    short_data = audio_2
    swapped = False
    if len(audio_1.time_amplitudes) < len(audio_2.time_amplitudes):
        long_data = audio_2
        short_data = audio_1
        swapped = True

    # For now, we'll overlay the shorter piece at the beginning of the longer one. This shouldn't be too hard to change later if need be.
    # First, we normalize the vectors by their peak-to-peak distances (max point - min point)
    long_data_p2p = np.max(long_data.time_amplitudes) - np.min(long_data.time_amplitudes)
    short_data_p2p = np.max(short_data.time_amplitudes) - np.min(short_data.time_amplitudes)

    long_data_normalized = copy.deepcopy(long_data.time_amplitudes) / long_data_p2p
    short_data_normalized = copy.deepcopy(short_data.time_amplitudes)/short_data_p2p

    new_data = long_data_normalized
    new_data[0:short_data.time_amplitudes.shape[0]] += short_data_normalized
    # scale back up by the average of the peak-to-peak distances in the audio sources
    # Note: This may not work very well if one of the samples is really quiet
    rescaling_factor = (long_data_p2p + short_data_p2p)/2
    new_data *= rescaling_factor
    combined = AudioData(manual_init=(long_data.sampling_freq, new_data))
    output1 = AudioData(manual_init=(long_data.sampling_freq, long_data_normalized*rescaling_factor))
    output2 = AudioData(manual_init=(long_data.sampling_freq, short_data_normalized*rescaling_factor))
    if swapped:
        output1, output2 = output2, output1
    return combined, output1, output2


# returns a *separate* downsampled instance, leaving the parameter audiodata unchanged
# For now, we only support downsampling to an integer multiple of the original sample period.
# WARNING: downsampling by too much may lead to significant aliasing effects!
# An aliasing problem can be diagnosed by comparing corresponding frequency terms in the old sequence's FFT and the new
# sequence's FFT. Low-pass filters can be used before downsampling to avoid the effects of aliasing.
def downsample(audiodata: AudioData, divisor: int) -> AudioData:
    if divisor <= 0:
        raise ValueError("The divisor parameter must be a positive integer")
    if audiodata.sampling_freq % divisor != 0:
        raise ValueError("The original sampling frequency isn't cleanly divisible by that divisor.")
    new_frequency = audiodata.sampling_freq//divisor
    new_time_amplitudes = audiodata.time_amplitudes[0::divisor]
    return AudioData(manual_init=(new_frequency, new_time_amplitudes))


# Given a long audiodata object, slices it up into snippets of length 'snippet_len_ms' milliseconds. Excess audio data is discarded.
# All of the resulting audiodata objects are pickled and saved as different files in the provided directory.
# Optionally, an overlap factor (between 0 and 1, excluding 1) may be specified. If the overlap factor > 0,
# two adjacent snippets will share that fraction of samples, rounded down to the nearest sample.
# You may want to downsample before invoking this.
def cut_into_snippets(audiodata: AudioData, dir_name: str, snippet_len_ms: float, snippet_overlap: float = 0.):
    if snippet_overlap < 0 or snippet_overlap >= 1:
        raise ValueError("snippet_overlap must be in [0,1). Provided value, {}, is illegal.".format(snippet_overlap))
    samples_per_snippet = int(snippet_len_ms/1000 * audiodata.sampling_freq)
    overlap_samples = int(samples_per_snippet * snippet_overlap)

    num_snippets_to_create = len(audiodata.time_amplitudes - samples_per_snippet)//(samples_per_snippet - overlap_samples)
    est_disk_usage = (num_snippets_to_create * samples_per_snippet * 2)/(1024**2)  # each sample is 2 bytes, 1 MB = 1024**2 bytes. This approach ignores file headers.
    print("Creating {} pickled audiodata files. Lower bound on new disk usage from this operation: {:.4f} MB".format(num_snippets_to_create, est_disk_usage))

    filenum = 0
    for i in range(0, len(audiodata.time_amplitudes) - samples_per_snippet, samples_per_snippet - overlap_samples):
        end_idx = i + samples_per_snippet
        snip_audiodata: AudioData = AudioData(manual_init=(audiodata.sampling_freq, audiodata.time_amplitudes[i:end_idx]))
        snip_audiodata.save(dir_name + "/snippet{}.pkl".format(filenum))
        filenum += 1

# creates a new audiodata object with the first 'trim_start' seconds removed and the last 'trim_start' seconds removed.
def trim(audiodata: AudioData, trim_start: float = 0., trim_end: float = 0) -> AudioData:
    samples_start = int(trim_start*audiodata.sampling_freq)
    samples_end = len(audiodata.time_amplitudes) - int(trim_end*audiodata.sampling_freq)
    return AudioData(manual_init=(audiodata.sampling_freq, audiodata.time_amplitudes[samples_start:samples_end]))
