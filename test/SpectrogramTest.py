import unittest
from src.AudioDataUtils import AudioData
from src.StftData import StftData


class SpectrogramTestCase(unittest.TestCase):
    def test_spectrogram(self):
        rec = AudioData("example_data/simple.wav")
        stft = StftData(audiodata=rec)
        stft.save_spectrogram("test_data/pic.png", show=False)


if __name__ == "__main__":
    unittest.main()