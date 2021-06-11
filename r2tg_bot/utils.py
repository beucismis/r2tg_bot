import os
import subprocess
import configparser
import urllib.request
from shutil import which


def check_ffmpeg():
    """Check if ffmpeg exists on PATH

    Returns:
        bool: True for exists
    """

    return which("ffmpeg") is not None


def get_config():
    """Get the configuration file

    Returns:
        class: Configuration parser object
    """

    config = configparser.ConfigParser()
    files = config.read("config.ini")

    if not len(files):
        raise FileNotFoundError("Config file not found!")

    return config


def normalize_name(name):
    """Make lower case all characters

    Args:
        name (str): User or subreddit name

    Retrun:
        str: Lower case user name
    """

    return name.lower()


def get_text_of_parent(comment):
    """Gets parent text of the submission or comment

    Args:
        comment (class): Reddit comment

    Returns:
        str: Text of parent or null
    """

    parent = comment.parent()

    if isinstance(parent, Submission):
        return parent.selftext
    elif isinstance(parent, Comment):
        return parent.body

    return ""


def author_name(comment):
    """Returns the author name

    Args:
        comment (class): Reddit comment

    Returns:
        str: If deleted '[deleted]'
        if not deleted lower case author name
    """

    if comment.author is None:
        return "[deleted]"
    else:
        return normalize_name(comment.author.name)


def subreddit_name(comment):
    """Return the subreddit name

    Args:
        comment (class): Reddit comment

    Returns:
        str: Lower case subreddit name
    """

    return normalize_name(comment.subreddit.display_name)


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
