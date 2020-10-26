import unittest
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


if __name__ == "__main__":
    unittest.main()