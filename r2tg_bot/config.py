import logging


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
