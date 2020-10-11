import pickle

import numpy as np
from typing import Tuple, Optional
from scipy.io import wavfile
import AudioDataUtils


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
        AudioDataUtils.assert_wav_file(wav_filepath)
        fs, data = wavfile.read(wav_filepath)
        self.sampling_freq = fs
        # Save only the audio from the first channel. Later, it might be useful to extract multiple channels.
        # This comes with the sizable assumption that the voice data is in the first channel. If this turns out to be
        # untrue, we can try to superimpose all of the channels on top of each other.
        self.time_amplitudes = data[:, 0].astype(np.float32)

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump((self.sampling_freq, self.time_amplitudes), file, -1)

    def load(self, filepath):
        with open(filepath, 'rb') as file:
            self.sampling_freq, self.time_amplitudes = pickle.load(file)

