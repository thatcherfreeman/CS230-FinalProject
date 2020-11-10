import unittest

import DataPrep
from src.AudioDataUtils import AudioData, play, superimpose, downsample, cut_into_snippets, trim
from src.StftData import StftData, StftArgs

PATH_TO_SIMPLE_WAV = "example_data/simple.wav"
PATH_TO_ALLSTAR_WAV = "example_data/allstar.wav"
PATH_TO_BIDEN_PKL = "example_data/biden_short.pkl"


class AudioDataTestCase(unittest.TestCase):
    def test_load_wav_data(self):
        audiodata: AudioData = AudioData(wav_filepath=PATH_TO_SIMPLE_WAV)
        play(audiodata)

    def test_pickle_audio_data(self):
        audiodata: AudioData = AudioData(wav_filepath=PATH_TO_SIMPLE_WAV)
        audiodata.save("test_data/pickled_audiodata.pkl")
        reloaded: audiodata = AudioData(pickled_filepath="test_data/pickled_audiodata.pkl")
        play(reloaded)

    def test_superimpose_audio_data(self):
        simple: AudioData = AudioData(wav_filepath=PATH_TO_SIMPLE_WAV)
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        superimposed, _, _ = superimpose(simple, allstar)
        play(superimposed)

    def test_downsample_audio_data(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        downsampled: AudioData = downsample(allstar, 4)
        play(downsampled)

    def test_stft_and_back(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        print("Playing original...")
        play(allstar)
        allstar_freq: StftData = StftData(audiodata=allstar)
        allstar_reconstruction = allstar_freq.invert()
        print("Playing reconstructed...")
        play(allstar_reconstruction)

    def test_trim_freq_data(self):
        biden = AudioData(pickled_filepath=PATH_TO_BIDEN_PKL)
        args = StftArgs(nperseg=1022, noverlap=511)
        freq_data = StftData(args=args, audiodata=biden)
        freq_data = DataPrep.trim_stft_data(freq_data)
        new_biden = freq_data.invert()
        play(new_biden)


if __name__ == '__main__':
    unittest.main()
