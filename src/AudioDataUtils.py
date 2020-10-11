import copy
import sys
import wave
import pyaudio
import numpy as np
from src.AudioData import AudioData

BYTES_PER_SAMPLE = 2
AUDIO_WRITE_CHUNK_SIZE = 1024


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


def superimpose(audio_1: AudioData, audio_2: AudioData) -> AudioData:
    if audio_1.sampling_freq != audio_2.sampling_freq:
        # It is technically possible to upsample/downsample audio, but that can introduce losses that complicate our efforts.
        # For now, let's see if we can get all of our audio sources at a standard sampling frequency.
        raise ValueError("Superimposing 2 AudioData sources with different sampling frequencies is unsupported.")
    long_data = audio_1
    short_data = audio_2
    if len(audio_1.time_amplitudes) < len(audio_2.time_amplitudes):
        long_data = audio_2
        short_data = audio_1

    # For now, we'll overlay the shorter piece at the beginning of the longer one. This shouldn't be too hard to change later if need be.
    # First, we normalize the vectors by their peak-to-peak distances (max point - min point)
    long_data_p2p = np.max(long_data.time_amplitudes) - np.min(long_data.time_amplitudes)
    short_data_p2p = np.max(short_data.time_amplitudes) - np.min(short_data.time_amplitudes)
    new_data = copy.deepcopy(long_data.time_amplitudes) / long_data_p2p
    new_data[0:short_data.time_amplitudes.shape[0]] += short_data.time_amplitudes/short_data_p2p
    # scale back up by the average of the peak-to-peak distances in the audio sources
    # Note: This may not work very well if one of the samples is really quiet
    new_data *= (long_data_p2p + short_data_p2p)/2
    return AudioData(manual_init=(long_data.sampling_freq, new_data))
