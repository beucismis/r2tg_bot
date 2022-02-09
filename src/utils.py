import os
import subprocess
import configparser
import urllib.request
from praw import Reddit
from shutil import which
from pyrogram import Client as Telegram
from praw.models import Comment, Submission


def check_ffmpeg():
    return which("ffmpeg") is not None


def get_config():
    config = configparser.ConfigParser()
    files = config.read("src/config.ini")

    if not len(files):
        raise FileNotFoundError("Config file not found!")

    return config


def normalize_name(name):
    return name.lower()


def get_text_of_parent(comment):
    parent = comment.parent()

    if isinstance(parent, Submission):
        return parent.selftext
    elif isinstance(parent, Comment):
        return parent.body

    return ""


def author_name(comment):
    if comment.author is None:
        return "[deleted]"
    else:
        return normalize_name(comment.author.name)


def subreddit_name(comment):
    return normalize_name(comment.subreddit.display_name)


def download(url, filename):
    urllib.request.urlretrieve(url, filename=filename)


def merge(video, audio):
    subprocess.call(
        f"ffmpeg -i {video} -i {audio} -c:v copy -c:a aac output.mp4 2>&1",
        shell=True,
    )
    os.remove(f"{video}")
    os.remove(f"{audio}")


def reddit_session():
    config = get_config()

    return Reddit(
        username=config.get("reddit", "username"),
        password=config.get("reddit", "password"),
        user_agent=config.get("reddit", "user_agent"),
        client_id=config.get("reddit", "client_id"),
        client_secret=config.get("reddit", "client_secret"),
    )


def telegram_session():
    config = get_config()

    return Telegram(
        session_name=config.get("telegram", "session_name"),
        api_id=config.getint("telegram", "api_id"),
        api_hash=config.get("telegram", "api_hash"),
    )
