import argparse
from typing import List
import numpy as np
import torch
from torch import nn

import model_utils
from AudioDataUtils import AudioData, downsample, audiodata_to_wav
from StftData import StftArgs, StftData

CD_QUALITY_SAMPLING_FREQ = 44100
DEFAULT_DOWNSAMPLE_FACTOR = 3
TARGET_SAMPLING_FREQ = CD_QUALITY_SAMPLING_FREQ//DEFAULT_DOWNSAMPLE_FACTOR
DEFAULT_STFT_ARGS: StftArgs = StftArgs(nperseg=1022, noverlap=511)
DEFAULT_NUM_SAMPLES_PER_SEGMENT = 511 * 127


"""Given a path to a .wav file, apply the model to remove Donald Trump's voice, then save the output as another .wav file.
Alpha is the cutoff threshold for the output of the sigmoid functions. Returns an AudioData object for convenience."""
def process_through_model(path_to_input_wav: str, path_to_output: str, model: nn.Module, args: argparse.Namespace) -> AudioData:
    # 1. create AudioData object from input
    full_input_audiodata: AudioData = AudioData(wav_filepath=path_to_input_wav)
    if full_input_audiodata.sampling_freq != CD_QUALITY_SAMPLING_FREQ and full_input_audiodata.sampling_freq != TARGET_SAMPLING_FREQ:
        raise ValueError("The input .wav file should have a "
                         "sampling frequency of either 44.1 kHz or 44.1/3 kHz, but it has {} kHz instead".format(full_input_audiodata.sampling_freq/1000))
    if full_input_audiodata.sampling_freq == CD_QUALITY_SAMPLING_FREQ:
        full_input_audiodata = downsample(full_input_audiodata, DEFAULT_DOWNSAMPLE_FACTOR)

    # 2. split input data into non-overlapping segments. This will truncate a small chunk (<4.5s) of the input audio.
    # Then, convert the segments to the frequency domain.
    input_segments = list()
    num_samples_per_segment = DEFAULT_NUM_SAMPLES_PER_SEGMENT
    for i in range(0, len(full_input_audiodata.time_amplitudes)//num_samples_per_segment):
        begin_idx = i*num_samples_per_segment
        end_idx = begin_idx + num_samples_per_segment
        next_segment: AudioData = AudioData(manual_init=(full_input_audiodata.sampling_freq,
                                                         full_input_audiodata.time_amplitudes[begin_idx:end_idx]))
        next_segment_freq: StftData = StftData(args=DEFAULT_STFT_ARGS, audiodata=next_segment)
        input_segments.append(next_segment_freq)

    # 3. Run the model on the input segments
    num_freqs = input_segments[0].sample_freqs.shape[0]
    num_windows = input_segments[0].segment_times.shape[0]
    input_freq_domain = np.zeros((len(input_segments), 1, num_freqs, num_windows), dtype=np.complex64)

    for i in range(len(input_segments)):
        input_freq_domain[i, 0, :, :] = input_segments[i].data

    output_segments = apply_model(input_freq_domain, model, input_segments[0], args)

    # 4. Concatenate the output segments into an output AudioData object
    output_time_amplitudes = np.zeros((num_samples_per_segment * len(output_segments)),)
    for i in range(0, len(output_segments)):
        begin_idx = i*num_samples_per_segment
        end_idx = begin_idx + num_samples_per_segment
        output_time_amplitudes[begin_idx:end_idx] = output_segments[i].time_amplitudes

    output_audio: AudioData = AudioData(manual_init=(TARGET_SAMPLING_FREQ, output_time_amplitudes))

    # 5. convert output to wav file and save it to wav filepath
    # TODO: implement this, for now it will saved as a pkl file
    # output_audio.save(path_to_output)
    audiodata_to_wav(output_audio, path_to_output)
    return output_audio


"""Given an (m, 1, freqs, windows) numpy array and a model, run the model on the input data and transform the results back into the time domain.
The 'example_stft' parameter is used to help reconstruct StftData objects to be converted to the time domain. Any StftData object with the same
'data' shape and sample frequency will work for this."""
def apply_model(input: np.ndarray, model: nn.Module, example_stft: StftData, args: argparse.Namespace) -> List[AudioData]:
    device = model_utils.get_device()
    input_tensor = torch.tensor(input, dtype=torch.complex64)
    input_mags = input_tensor.abs().to(device)
    predictions, _ = model(input_mags)
    if args.nonboolean_mask:
        predicted_mask = torch.clamp(predictions / input_mags, 0, 1)
    else:
        predicted_mask = torch.ones_like(predictions) * (torch.clamp(predictions / input_mags, 0, 1) > args.alpha)
    output_freqs = input_tensor * (predicted_mask.detach().numpy())

    # Convert the outputs back to the time domain
    output_time_data = list()
    for i in range(output_freqs.shape[0]):
        freq_data = StftData(args=example_stft.args,
                 manual_init=(output_freqs[i, 0, :, :], example_stft.sample_freqs, example_stft.segment_times, example_stft.fs))
        output_time_data.append(freq_data.invert())

    return output_time_data
