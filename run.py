#!/usr/bin/python3

from src.bot import run
from src.utils import check_ffmpeg


if __name__ == "__main__":
    if not check_ffmpeg():
        raise PackageNotFound("FFmpeg not found!")

    print("Bot running...")
    run()
