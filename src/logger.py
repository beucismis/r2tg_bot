import os
import logging
from logging.handlers import RotatingFileHandler


path = os.path.dirname(os.path.abspath(__file__))


class Handler(RotatingFileHandler):

    LEVEL = logging.INFO

    def __init__(self):
        RotatingFileHandler.__init__(self, os.path.join(path, "logs", "r2tg_bot.log"))
        self.backupCount = 5
        self.encoding = "UTF-8"
        self.maxBytes = 5_000_000

        datefmt = "%Y-%m-%d %H:%M:%S"
        fmt = "[%(asctime)s][%(levelname)s] - %(message)s"
        self.setFormatter(logging.Formatter(fmt, datefmt))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(Handler.LEVEL)
    logger.addHandler(Handler())

    return logger
