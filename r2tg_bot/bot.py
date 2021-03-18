import time
import logging
from os import listdir
from datetime import datetime
from logging.handlers import RotatingFileHandler

import praw.exceptions
from praw.models import Comment, Submission

import config as c
from util import get_reddit, get_telegram, download_media


__import__("warnings").filterwarnings("ignore")


logger = logging.getLogger(c.LOGGER_NAME)
logger.setLevel(c.LOG_LEVEL)
handler = RotatingFileHandler(
    c.LOG_FILE_PATH,
    encoding="utf-8",
    maxBytes=c.MAX_BYTES_PER_LOG,
    backupCount=c.NUM_LOG_FILES_TO_KEEP,
)
logger.addHandler(handler)
handler.setFormatter(logging.Formatter(c.FORMAT))


def get_text_of_parent(comment):
    parent = comment.parent()

    if isinstance(parent, Submission):
        return parent.selftext
    elif isinstance(parent, Comment):
        return parent.body

    return ""


def author_name(comment):
    return (
        "[deleted]" if comment.author is None else c.normalize_name(comment.author.name)
    )


def subreddit_name(comment):
    return c.normalize_name(comment.subreddit.display_name)


class R2TG_BOT:

    COMMENT_LOG_INDENT = 4
    MAX_NUM_TAGS_PER_USER_IN_CHAIN = 3

    def __init__(self, reddit, telegram):
        self._reddit = reddit
        self._telegram = telegram
        self._inbox = reddit.inbox
        self._bot_name = reddit.user.me().name.lower()
        self._tag_for_bot = "u/" + self._bot_name

        self.good_bot_strs = ["good bot", "iyi bot", "cici bot"]
        self.bad_bot_strs = ["bad bot", "kötü bot"]

    def reply_to_username_mentions(self):
        logger.info("Reading inbox...")

        for mention in self._inbox.unread(limit=c.LIMIT_ON_INBOX):
            lower = mention.body.lower()

            if isinstance(mention, Comment) and self._was_tagged_in(mention):
                try:
                    logger.info("Received comment:")
                    self._reply_to_comment(mention)
                except Exception as e:
                    logger.error(
                        "Encountered exception '{}' while attempting to respond to comment: {}".format(
                            type(e).__name__, str(e)
                        )
                    )

            elif lower in self.good_bot_strs:
                self._inbox.mark_read([mention])
                logger.info("Good bot.")
                mention.reply("ヽ(•‿•)ノ")

            elif lower in self.bad_bot_strs:
                self._inbox.mark_read([mention])
                logger.info("Bad bot.")
                mention.reply("( ._.)")

        logger.info("Finished reading inbox.")
        logger.info("=" * 50)

    def _was_tagged_in(self, mention):
        return self._tag_for_bot in mention.body.lower()

    def _reply_to_comment(self, comment):
        self._inbox.mark_read([comment])

        logger.info("Author is u/" + author_name(comment) + ".")
        logger.info("Subreddit is r/" + subreddit_name(comment) + ".")

        should_reply = True

        if self._too_many_tagged(comment):
            should_reply = False
            logger.info(
                "Author has tagged too many times in this comment chain, ignoring."
            )

        if self._author_is_in_blacklist(comment):
            should_reply = False
            logger.info("Author is blacklisted, ignoring.")

        if self._subreddit_is_in_blacklist(comment):
            should_reply = False
            logger.info("Subreddit is blacklisted, ignoring.")

        if comment.submission.over_18:
            should_reply = False
            logger.info("Submission is NSFW, ignoring.")
            comment.reply("Yes video but NSFW. I'm so sorry... \n\n" + c.INFO)

        got_rate_limited = False

        if should_reply:
            got_rate_limited = self._attempt_reply(comment)

        if got_rate_limited:
            logger.warning("Got rate-limited, will try again in next pass of inbox.")
            self._wait_for_rate_limiting_to_pass()
            self._inbox.mark_unread([comment])

        logger.info("Comment processed.")

    def _too_many_tagged(self, mention):
        tags = 0
        comment = mention

        while not comment.is_root:
            if author_name(comment) == author_name(mention) and self._was_tagged_in(
                comment
            ):
                tags += 1
            comment = comment.parent()

        return tags > R2TG_BOT.MAX_NUM_TAGS_PER_USER_IN_CHAIN

    def _author_is_in_blacklist(self, comment):
        return author_name(comment) in c.USER_BLACKLIST

    def _subreddit_is_in_blacklist(self, comment):
        return subreddit_name(comment) in c.SUBREDDIT_BLACKLIST

    def _attempt_reply(self, mention):
        text_of_parent = get_text_of_parent(mention)
        submission = mention.submission
        file_name = submission.url.split("/")[-1]

        logger.info("Downloading video...")
        download_media(submission.url, file_name)
        # logger.info("Text of parent is: " + text_of_parent)
        logger.info("Uploading video...")

        with self._telegram:
            self._telegram.send_video(
                c.DEFAULT_TG_CHANNEL,
                c.MEDIA_PATH + "/" + file_name + ".mp4",
                caption=(
                    "**Title:** {0} \n**Link:** {1} \n**"
                    "Subreddit:** r/#{2} \n**Author:** u/#{3}".format(
                        submission.title,
                        submission.url,
                        submission.subreddit,
                        submission.author,
                    )
                ),
            )
        logger.info("Done.")

        try:
            mention.reply(
                "Yes, video. I'm ready, sending to Telegram... \n\n"
                "### [Upload via {0}]({1}) \n".format(
                    c.DEFAULT_TG_CHANNEL, c.DEFAULT_TG_CHANNEL_URL
                )
                + c.INFO
            )
        except praw.exceptions.APIException as e:
            logger.warning("API exception: " + e.message)
            if e.error_type == "RATELIMIT":
                return True

        return False

    def _wait_for_rate_limiting_to_pass(self):
        logger.warning(
            "Waiting {} seconds for rate-limiting to wear off.".format(
                c.SECONDS_TO_WAIT_AFTER_RATE_LIMITING
            )
        )
        time.sleep(c.SECONDS_TO_WAIT_AFTER_RATE_LIMITING)


def run_the_bot():
    bot = R2TG_BOT(get_reddit(), get_telegram())

    while True:
        try:
            bot.reply_to_username_mentions()
        except Exception as e:
            logger.error("Got an unexpected error when reading inbox: " + str(e))

        time.sleep(c.SECONDS_BETWEEN_RUNS)
