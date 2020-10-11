import AudioDataUtils
from AudioData import AudioData

if __name__ == "__main__":
    audiodata: AudioData = AudioData(wav_filepath="../example_data/simple.wav")
    AudioDataUtils.play(audiodata)

    audiodata.save("../test_data/pickled_audiodata.pkl")
    audiodata2: audiodata = AudioData(pickled_filepath="../test_data/pickled_audiodata.pkl")
    AudioDataUtils.play(audiodata2)

    allstar: AudioData = AudioData(wav_filepath="../example_data/allstar.wav")

    AudioDataUtils.play(AudioDataUtils.superimpose(audiodata, allstar))