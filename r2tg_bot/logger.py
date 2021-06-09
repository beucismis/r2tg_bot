import logging
from logging.handlers import RotatingFileHandler


class Handler(RotatingFileHandler):

    level = logging.INFO

    def __init__(self):
        RotatingFileHandler.__init__(self, "r2tg_bot.log")
        self.backupCount = 5
        self.encoding = "UTF-8"
        self.maxBytes = 5_000_000

        datefmt = "%Y-%m-%d %H:%M:%S"
        fmt = "[%(asctime)s][%(levelname)s] - %(message)s"
        self.setFormatter(logging.Formatter(fmt, datefmt))
