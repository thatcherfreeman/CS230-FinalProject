import pickle
from typing import Optional, Any, Tuple
import numpy as np # type: ignore
from scipy import signal # type: ignore
from AudioDataUtils import AudioData
import matplotlib.pyplot as plt # type: ignore


# parameters used for stft (needed for inverse stft)
class StftArgs:
    window: Optional[Any]
    # Even those these two values have defaults, it's recommended to manually tune them
    nperseg: Optional[int]
    noverlap: Optional[int]

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
    fs: float  # Sampling frequency of the audio in the time domain
    args: StftArgs

    def __init__(self, args: Optional[StftArgs] = None, audiodata: Optional[AudioData] = None,
                 pickle_file: Optional[str] = None,
                 # The arguments to 'manual_init' are in the following order: data, sample_freqs, segment_times, fs
                 manual_init: Optional[Tuple[np.ndarray, np.ndarray, np.ndarray, float]] = None):
        if audiodata is not None:
            self.args = args # type: ignore
            if self.args is None:
                self.args = StftArgs()
            self.fs = audiodata.sampling_freq
            self.sample_freqs, self.segment_times, self.data =\
                signal.stft(audiodata.time_amplitudes, fs=self.fs, window=self.args.window,
                            nperseg=self.args.nperseg, noverlap=self.args.noverlap)
        elif pickle_file is not None:
            self.load(pickle_file)
        elif manual_init is not None:
            self.args = args
            if self.args is None:
                raise ValueError("Some manual_init data has been provided, so you almost certainly want to pass StftArgs as well.")
            self.data = manual_init[0]
            self.sample_freqs = manual_init[1]
            self.segment_times = manual_init[2]
            self.fs = manual_init[3]
        else:
            raise ValueError("You must provide either a pickle file, some STFT args and audio data, "
                             "or a manual_init tuple of the form (data, sample_freqs, segment_times, fs).")

    """Transforms the frequency data back into the time domain"""
    def invert(self) -> AudioData:
        _, time_amplitudes = signal.istft(self.data, fs=self.fs, window=self.args.window,
                                         nperseg= self.args.nperseg, noverlap=self.args.noverlap)
        return AudioData(manual_init=(int(self.fs), time_amplitudes))

    """Saves the scipy-generated frequency spectrogram of the data to a file."""
    def save_spectrogram(self, filepath: Optional[str]=None, show: bool = False):
        if str(self.data.dtype) == 'float32':
            # assume mask
            magnitude = np.abs(self.data).astype(np.float32)
        else:
            magnitude = np.clip(np.log(np.abs(self.data).astype(np.float32)), 0, 10)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        plt.imshow(magnitude, aspect='auto', cmap='viridis')
        plt.gca().invert_yaxis()  # put high freq on top

        ax.set_axis_off()
        ax2 = fig.add_axes(ax.get_position())
        ax2.patch.set_alpha(0)
        ax2.set_xlim(left=self.segment_times[0], right=self.segment_times[-1])
        ax2.set_ylim(bottom=self.segment_times[0], top=self.sample_freqs[-1])
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (seconds)")
        if filepath is not None:
            plt.savefig(filepath)
        if show:
            plt.show()

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump((self.sample_freqs, self.segment_times, self.data, self.fs, self.args), file, -1)

    def load(self, filepath):
        with open(filepath, 'rb') as file:
            self.sample_freqs, self.segment_times, self.data, self.fs, self.args = pickle.load(file)
