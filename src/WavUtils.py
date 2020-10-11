import numpy
import pyaudio
import wave
from scipy.io.wavfile import read

def play(wav_filepath):
    STREAM_CHUNK_SIZE = 1024

    wf = wave.open(wav_filepath, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(STREAM_CHUNK_SIZE)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(STREAM_CHUNK_SIZE)

    stream.stop_stream()
    stream.close()
    p.terminate()


def transform_chunk(audio):
    if len(audio) == 0:
        return audio
    audio_arr = numpy.frombuffer(audio, dtype=numpy.int16).astype(numpy.float32)  # can do /2**15 to normalize

    num_same = 0
    for i in range(0, len(audio_arr), 2):
        if audio_arr[i] == audio_arr[i + 1]:
            num_same += 1
        audio_arr[i] = 0

    audio_fft = numpy.fft.rfft(audio_arr)

    # audio manipulation
    # for i in range(0, len(audio_fft)):
    #     if i <= len(audio_fft)/5: # and i >= len(audio_fft)/30:
    #         audio_fft[i] = 0

    audio_manipulated = numpy.fft.irfft(audio_fft)

    return audio_manipulated.astype(numpy.int16).tobytes()