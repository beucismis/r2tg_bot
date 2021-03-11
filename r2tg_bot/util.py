import subprocess

import praw
import pyrogram

import config as c


def get_reddit():
    return praw.Reddit("bot")


def get_telegram():
    return pyrogram.Client("r2tg_bot", config_file="pyrogram.ini")


def download_media(url, file_name):
    subprocess.run(
        [
            f"ffmpeg -i {url}/DASHPlaylist.mpd -c copy {c.MEDIA_PATH}/{file_name}.mp4 2> /dev/null"
        ],
        shell=True,
    )
