import logging
from logging.handlers import RotatingFileHandler


class Handler(RotatingFileHandler):
    """The specified file is opened and used as the stream for logging"""

    LEVEL = logging.INFO

    def __init__(self):
        RotatingFileHandler.__init__(self, "r2tg_bot.log")
        self.backupCount = 5
        self.encoding = "UTF-8"
        self.maxBytes = 5_000_000

        datefmt = "%Y-%m-%d %H:%M:%S"
        fmt = "[%(asctime)s][%(levelname)s] - %(message)s"
        self.setFormatter(logging.Formatter(fmt, datefmt))


def get_logger(name):
    """Return a logger with the specified name

    Args:
        name (str): Name for logger

    Returns:
        class: Loggers have following attributes and methods
    """

    logger = logging.getLogger(name)
    logger.setLevel(Handler.LEVEL)
    logger.addHandler(Handler())

    return logger
