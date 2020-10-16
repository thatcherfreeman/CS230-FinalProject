import unittest
import AudioDataUtils
from AudioData import AudioData
from StftData import StftData, StftArgs

PATH_TO_SIMPLE_WAV = "../example_data/simple.wav"
PATH_TO_ALLSTAR_WAV = "../example_data/allstar.wav"


class AudioDataTestCase(unittest.TestCase):
    def test_load_wav_data(self):
        audiodata: AudioData = AudioData(wav_filepath=PATH_TO_SIMPLE_WAV)
        AudioDataUtils.play(audiodata)

    def test_pickle_audio_data(self):
        audiodata: AudioData = AudioData(wav_filepath=PATH_TO_SIMPLE_WAV)
        audiodata.save("../test_data/pickled_audiodata.pkl")
        reloaded: audiodata = AudioData(pickled_filepath="../test_data/pickled_audiodata.pkl")
        AudioDataUtils.play(reloaded)

    def test_superimpose_audio_data(self):
        simple: AudioData = AudioData(wav_filepath=PATH_TO_SIMPLE_WAV)
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        superimposed: AudioData = AudioDataUtils.superimpose(simple, allstar)
        AudioDataUtils.play(superimposed)

    def test_downsample_audio_data(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        downsampled: AudioData = AudioDataUtils.downsample(allstar, 4)
        AudioDataUtils.play(downsampled)

    def test_stft_and_back(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        print("Playing original...")
        AudioDataUtils.play(allstar)
        allstar_freq: StftData = StftData(audiodata=allstar)
        allstar_reconstruction = allstar_freq.invert()
        print("Playing reconstructed...")
        AudioDataUtils.play(allstar_reconstruction)

    def test_pickle_stft_and_back(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        allstar_freq: StftData = StftData(audiodata=allstar, args=StftArgs(nperseg=1024, noverlap=3))
        allstar_freq.save("../test_data/pickled_freqdata.pkl")
        loaded_freq: StftData = StftData(pickle_file="../test_data/pickled_freqdata.pkl")
        allstar_reconstruction = loaded_freq.invert()
        AudioDataUtils.play(allstar_reconstruction)


if __name__ == '__main__':
    unittest.main()
