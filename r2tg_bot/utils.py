import os
import subprocess
import urllib.request
from shutil import which


def check_ffmpeg():
    """Check if ffmpeg exists on PATH

    Returns:
        bool: True for exists
    """

    return which("ffmpeg") is not None


def download(url, filename):
    """Download the given url

    Args:
        url (str): Link to download file
        filename (str): Name to save the file to
    """

    urllib.request.urlretrieve(url, filename=filename)


def merge(video, audio):
    """Merges video and audio file with ffmpeg

    Args:
        video (str): Video file name
        audio (str): Audio file name
    """

    # ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4
    subprocess.call(
        "ffmpeg -i {} -i {} -c:v copy -c:a aac {}".format(video, audio, "output.mp4"),
        shell=True,
    )

    os.remove("video.mp4")
    os.remove("audio.mp4")
