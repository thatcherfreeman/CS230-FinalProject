import os
import unittest

from src.AudioDataUtils import AudioData, play, superimpose, downsample, cut_into_snippets, trim
from src.StftData import StftData, StftArgs

PATH_TO_SIMPLE_WAV = "example_data/simple.wav"
PATH_TO_ALLSTAR_WAV = "example_data/allstar.wav"


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
        superimposed: AudioData = superimpose(simple, allstar)
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

    def test_pickle_stft_and_back(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        allstar_freq: StftData = StftData(audiodata=allstar, args=StftArgs(nperseg=1024, noverlap=3))
        allstar_freq.save("test_data/pickled_freqdata.pkl")
        loaded_freq: StftData = StftData(pickle_file="test_data/pickled_freqdata.pkl")
        allstar_reconstruction = loaded_freq.invert()
        play(allstar_reconstruction)

    def test_cut_into_snippets(self):
        snippet_dir = "test_data/snippets"

        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        cut_into_snippets(allstar, snippet_dir, 500, snippet_overlap=0.4)
        for filename in os.listdir(snippet_dir):
            snip_data: AudioData = AudioData(pickled_filepath=snippet_dir + "/" + filename)
            play(snip_data)

    def test_trim_audio_data(self):
        allstar: AudioData = AudioData(wav_filepath=PATH_TO_ALLSTAR_WAV)
        trimmed: AudioData = trim(allstar, trim_start=0.5, trim_end=0.4)
        play(trimmed)


if __name__ == '__main__':
    unittest.main()
