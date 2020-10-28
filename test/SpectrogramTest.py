import unittest
import numpy as np

from src.AudioDataUtils import AudioData
from src.StftData import StftData



class SpectrogramTestCase(unittest.TestCase):
    def test_spectrogram(self):
        rec = AudioData("example_data/simple.wav")
        stft = StftData(audiodata=rec)
        stft.save_spectrogram("test_data/pic.png", show=False)
    def test_spectrogram_train_data(self):
        stft = StftData(pickle_file="example_data/combined_1001.pkl")
        stft.save_spectrogram("test_data/combined.png", show=False)
    def test_spectrogram_train_data_trump(self):
        stft = StftData(pickle_file="example_data/trump_1001.pkl")
        stft.save_spectrogram("test_data/trump.png", show=False)
    def test_spectrogram_train_data_biden(self):
        stft = StftData(pickle_file="example_data/biden_1001.pkl")
        stft.save_spectrogram("test_data/biden.png", show=False)
    def test_spectrogram_train_data_mask(self):
        stft_biden = StftData(pickle_file="example_data/biden_1001.pkl")
        stft_trump = StftData(pickle_file="example_data/trump_1001.pkl")
        stft_biden.data = np.ones_like(stft_biden.data, dtype=np.float32) * (np.abs(stft_biden.data) > np.abs(stft_trump.data))
        stft_biden.save_spectrogram("test_data/mask.png", show=False)
    def test_spectrogram_train_data_sep(self):
        stft_biden = StftData(pickle_file="example_data/biden_1001.pkl")
        stft_trump = StftData(pickle_file="example_data/trump_1001.pkl")
        stft_combined = StftData(pickle_file="example_data/combined_1001.pkl")
        stft_mask = StftData(pickle_file="example_data/biden_1001.pkl")
        stft_mask.data = np.ones_like(stft_biden.data, dtype=np.float32) * (np.abs(stft_biden.data) > np.abs(stft_trump.data))
        stft_combined.data = stft_mask.data * stft_combined.data
        stft_combined.save_spectrogram("test_data/biden_reconstructed.png", show=False)

if __name__ == "__main__":
    unittest.main()