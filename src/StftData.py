import pickle
from typing import Optional, Any
import numpy as np
from scipy import signal
from src.AudioDataUtils import AudioData
import matplotlib.pyplot as plt
from skimage.transform import resize


# parameters used for stft (needed for inverse stft)
class StftArgs:
    window: Optional[Any]
    nperseg: Optional[int]  # actually choosing this value is encouraged, it's quite important
    noverlap: Optional[int]  # this is not as important as nperseg but we should still play with it

    def __init__(self, nperseg: Optional[int] = None, window: Optional[Any] = 'hann',
                 noverlap:  Optional[int] = None):
        self.nperseg = nperseg
        self.window = window
        self.noverlap = noverlap


"""A object holding the output of the short-time-fourier-transform of a piece of audio data.
See https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html for details."""
class StftData:
    sample_freqs: np.ndarray
    segment_times: np.ndarray
    data: np.ndarray  # In the scipy docs, this field is referred to as 'Zxx'.
    fs: float
    args: StftArgs

    def __init__(self, args: Optional[StftArgs] = None, audiodata: Optional[AudioData] = None,
                 pickle_file: Optional[str] = None):
        if audiodata is not None:
            self.args = args
            if self.args is None:
                self.args = StftArgs()
            self.fs = audiodata.sampling_freq
            self.sample_freqs, self.segment_times, self.data =\
                signal.stft(audiodata.time_amplitudes, fs=self.fs, window=self.args.window,
                            nperseg=self.args.nperseg, noverlap=self.args.noverlap)
        elif pickle_file is not None:
            self.load(pickle_file)
        else:
            raise ValueError("You must provide either a pickle file or some STFT args and audio data.")

    """Transforms the frequency data back into the time domain"""
    def invert(self) -> AudioData:
        _, time_amplitudes = signal.istft(self.data, fs=self.fs, window=self.args.window,
                                         nperseg= self.args.nperseg, noverlap=self.args.noverlap)
        return AudioData(manual_init=(int(self.fs), time_amplitudes))

    """Saves the scipy-generated frequency spectrogram of the data to a file."""
    def save_spectrogram(self, filepath: str, show: bool = False):
        magnitude = np.clip(np.log(np.abs(self.data).astype(np.float32)), 0, 10)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        plt.imshow(magnitude, aspect='auto', cmap='viridis')
        plt.colorbar()
        plt.gca().invert_yaxis() # put high freq on top

        # Lie about axis limits lol
        ax.set_axis_off()
        ax2 = fig.add_axes(ax.get_position())
        ax2.patch.set_alpha(0)
        ax2.set_xlim(left=self.segment_times[0], right=self.segment_times[-1])
        ax2.set_ylim(bottom=self.segment_times[0], top=self.sample_freqs[-1])
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (seconds)")
        if show:
            plt.show()
        plt.savefig(filepath)

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump((self.sample_freqs, self.segment_times, self.data, self.fs, self.args), file, -1)

    def load(self, filepath):
        with open(filepath, 'rb') as file:
            self.sample_freqs, self.segment_times, self.data, self.fs, self.args = pickle.load(file)
