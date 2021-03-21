import subprocess

import praw
import pyrogram

import config as c


def get_reddit():
    """Returns the Reddit client class.

    Returns:
        class: praw.Reddit
    """
    return praw.Reddit("r2tg_bot")


def get_telegram():
    """Return the Telegram client class.

    Returns:
        class: pyrogram.Client
    """
    return pyrogram.Client("r2tg_bot", config_file="pyrogram.ini")


def download_media(url, file_name):
    """Download the Reddit media.

    Parameters:
        url (str): Media link
        file_name (str): File name to save

    Returns:
        int: 0
    """
    subprocess.run(
        [
            f"ffmpeg -i {0}/DASHPlaylist.mpd -c copy {1}/{2}.mp4 2> /dev/null".format(
                url, c.MEDIA_PATH, file_name
            )
        ],
        shell=True,
    )

    return 0
