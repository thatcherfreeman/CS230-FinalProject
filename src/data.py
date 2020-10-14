import os
import typing as t
import shutil
import json
import subprocess
from pytube import YouTube
from pytube.exceptions import RegexMatchError


def pull_audio(url: str) -> str:
    """Pull audio from YouTube videos."""
    max_retries = 3
    for _ in range(max_retries):
        try:
            audio_stream = (
                YouTube(url)
                .streams
                .filter(mime_type="audio/mp4")
                .first()
            )
            if not audio_stream:
                raise ValueError("No audio stream found.")
            return audio_stream.download(os.path.join("tmp", "mp4"), filename=url.split("=")[1])
        except RegexMatchError:
            raise ValueError("Invalid URL passed.")
        except json.decoder.JSONDecodeError:
            # thrown on bad request to YouTube
            pass


def to_wav(mp4_path: str, trim_left: t.Optional[int] = None, trim_right: t.Optional[int] = None) -> str:
    """Convert YouTube mp4 to wav, trimming as desired."""
    wav_filename = os.path.join("tmp", "wav", os.path.split(mp4_path)[-1].replace("mp4", "wav"))
    file_details = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", mp4_path
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    end_time = float(json.loads(file_details.stdout)["format"]["duration"])
    start_time = 0
    if trim_left:
        start_time = trim_left
    if trim_right:
        end_time -= trim_right
    subprocess.run([
        "ffmpeg", "-i", mp4_path, "-bitexact", "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1",
        "-ss", str(start_time), "-to", str(end_time), wav_filename
    ])
    return wav_filename


def concat_norm_wavs(wav_files: t.List[str]) -> str:
    """Concatenate converted wavs into one large file and normalize volume."""
    with open("./tmp/wav_list.txt", "w") as f:
        f.write("\n".join(map(lambda x: f"file '{x.replace('tmp/', '')}'", wav_files)))
    save_file = "./audio/concat.wav"
    # concat into a single file
    subprocess.run([
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', './tmp/wav_list.txt', '-c', 'copy', save_file
    ])
    # normalize audio levels
    normed_save = save_file.replace(".wav", "_loud_norm.wav")
    subprocess.run([
        "ffmpeg", "-i", save_file, "-filter:a", "loudnorm", normed_save
    ])
    return normed_save


def run_audio_pulls() -> str:
    """Pull audio files from URLs specified in speeches.json, convert to wav, concatenate, and normalize levels."""
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
        os.mkdir("./tmp/mp4")
        os.mkdir("./tmp/wav")
    if not os.path.exists("./audio"):
        os.mkdir("./audio")
    saved_wavs = []
    with open("speeches.json") as f:
        speeches = json.load(f)
    for speech in speeches['speeches']:
        saved_mp4 = pull_audio(speech['url'])
        saved_wavs.append(to_wav(saved_mp4, speech.get("trim_left_seconds"), speech.get("trim_right_seconds")))
    concat_wav = concat_norm_wavs(saved_wavs)
    shutil.rmtree("./tmp")
    return concat_wav


if __name__ == '__main__':
    run_audio_pulls()