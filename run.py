#!/usr/bin/python3

from src import bot, utils


if __name__ == "__main__":
    if not utils.check_ffmpeg():
        raise PackageNotFound("FFmpeg not found!")

    print("Bot running...")
    bot.run()
