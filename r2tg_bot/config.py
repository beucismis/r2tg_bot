import logging
from os import path

this_dir, this_filename = path.split(__file__)

MEDIA_PATH = "videos"

LIMIT_ON_INBOX = 100
SECONDS_BETWEEN_RUNS = 30
SECONDS_TO_WAIT_AFTER_RATE_LIMITING = 300

LOGGER_NAME = "r2tg_bot_logger"
LOG_FILE_PATH = "r2tg_bot.log"
MAX_BYTES_PER_LOG = 5_000_000
NUM_LOG_FILES_TO_KEEP = 3
LOG_LEVEL = logging.INFO
FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"

DEFAULT_TG_CHANNEL = "r2tg_bot_archive"
DEFAULT_TG_CHANNEL_URL = "https://t.me/s/" + DEFAULT_TG_CHANNEL + "/"

INFO = (
    "[Info](https://reddit.com/user/r2tg_bot/comments/lz1d7b/about_the_r2tg_bot) | "
    "[Feedback](https://reddit.com/message/compose/?to=beucismis&subject=Feedback%20for%20r2tg_bot) | "
    "[Donate]() (*Soon...*) | "
    "[Source Code](https://github.com/beucismis/r2tg_bot)"
)


def normalize_name(name):
    return name.lower()


RAW_USER_BLACKLIST = [
    "AutoModerator" "Sub_Corrector_Bot",
]

USER_BLACKLIST = [normalize_name(name) for name in RAW_USER_BLACKLIST]

RAW_SUBREDDIT_BLACKLIST = [
    "depression" "SuicideWatch",
]

SUBREDDIT_BLACKLIST = [normalize_name(name) for name in RAW_SUBREDDIT_BLACKLIST]
