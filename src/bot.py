import time
from . import utils
from . import logger
from os import listdir
import praw.exceptions
from datetime import datetime
from praw.models import Comment
from logging.handlers import RotatingFileHandler


__version__ = "0.7.0"
__author__ = "Adil Gürbüz"
__contact__ = "beucismis@tutamail.com"
__source__ = "https://github.com/beucismis/r2tg_bot"
__description__ = "A Reddit bot that uploads video or GIF files to Telegram"

config = utils.get_config()
logger = logger.get_logger(__name__)


class Bot:
    def __init__(self, reddit_session, telegram_session):
        self.reddit_session = reddit_session
        self.telegram_session = telegram_session
        self.inbox = reddit_session.inbox

        self.good_bot_strings = ["good bot", "iyi bot", "cici bot"]
        self.bad_bot_strings = ["bad bot", "kötü bot"]

    def tag_for_bot(self):
        me = self.reddit_session.user.me()
        
        return f"u/{me.name.lower()}"

    def reply_to_username_mentions(self):
        logger.info("Reading inbox...")

        for mention in self.inbox.unread(
            limit=config.getint("general", "limit_on_inbox")
        ):
            lower = mention.body.lower()

            if isinstance(mention, Comment) and self._was_tagged_in(mention):
                try:
                    logger.info("Received comment:")
                    self._reply_to_comment(mention)
                except Exception as e:
                    logger.error(f"'{type(e).__name__}': {e}")
            
            elif lower in self.good_bot_strings:
                self.inbox.mark_read([mention])
                logger.info("Good bot.")
                mention.reply("ヽ(•‿•)ノ")

            elif lower in self.bad_bot_strings:
                self.inbox.mark_read([mention])
                logger.info("Bad bot.")
                mention.reply("( ._.)")

        logger.info("Finished reading inbox.")
        logger.info("-" * 50)

    def _was_tagged_in(self, mention):
        return self.tag_for_bot() in mention.body.lower()

    def _reply_to_comment(self, comment):
        should_reply = True
        self.inbox.mark_read([comment])

        logger.info(f"Author is u/{utils.author_name(comment)}")
        logger.info(f"Subreddit is r/{utils.subreddit_name(comment)}")

        if self._too_many_tagged(comment):
            should_reply = False
            logger.info("Too many comments, ignoring.")

        if self._author_is_in_blacklist(comment):
            should_reply = False
            logger.info("Author is blacklisted, ignoring.")

        if self._subreddit_is_in_blacklist(comment):
            should_reply = False
            logger.info("Subreddit is blacklisted, ignoring.")

        if comment.submission.over_18:
            should_reply = False
            logger.info("Submission is NSFW, ignoring.")

        got_rate_limited = False

        if should_reply:
            got_rate_limited = self._attempt_reply(comment)

        if got_rate_limited:
            logger.warning("Got rate-limited, will try again in next pass of inbox.")
            self._wait_for_rate_limiting_to_pass()
            self.inbox.mark_unread([comment])

        logger.info("Comment processed.")

    def _too_many_tagged(self, mention):
        tags = 0
        comment = mention

        while not comment.is_root:
            if utils.author_name(comment) == utils.author_name(mention) and self._was_tagged_in(
                comment
            ):
                tags += 1
            comment = comment.parent()

        return tags > config.getint("general", "max_num_tags_per_user_in_chain")

    def _author_is_in_blacklist(self, comment):
        return utils.author_name(comment) in [
            utils.normalize_name(name)
            for name in config.get("blacklist", "users").split(",")
        ]

    def _subreddit_is_in_blacklist(self, comment):
        return utils.subreddit_name(comment) in [
            utils.normalize_name(name)
            for name in config.get("blacklist", "subreddits").split(",")
        ]

    def _attempt_reply(self, mention):
        is_audio = True
        submission = mention.submission
        media = submission.media
        text_of_parent = utils.get_text_of_parent(mention)
        file_name = submission.url.split("/")[-1]

        video_url = media["reddit_video"]["fallback_url"]
        audio_url = (
            f"{video_url.split('DASH')[0]}DASH_audio.mp4?{video_url.split('?')[-1]}"
        )

        logger.info("Downloading video...")
        utils.download(video_url, f"{file_name}_video.mp4")

        try:
            logger.info("Downloading audio...")
            utils.download(audio_url, f"{file_name}_audio.mp4")
        except:
            is_audio = False
            logger.info("Downloading audio... Skip.")

        if is_audio:
            logger.info("Merged...")
            utils.merge(f"{file_name}_video.mp4", f"{file_name}_audio.mp4")

        logger.info("Uploading video...")
        default_telegram_channel = config.get("general", "default_telegram_channel")

        with self.telegram_session:
            message = self.telegram_session.send_video(
                chat_id=config.get("general", "default_telegram_channel"),
                video="output.mp4",
                caption=(
                    f"**Title:** {submission.title}\n"
                    f"**Link:** {submission.url}\n"
                    f"**Subreddit:** r/#{submission.subreddit}\n"
                    f"**Author:** u/#{submission.author}"
                ),
            )

        logger.info("Done.")
        logger.info("-" * 50)

        try:
            mention.reply(
                "Yes, video. I'm ready, sending to Telegram...\n\n"
                f"### [Upload via {default_telegram_channel}]"
                f"(https://t.me/s/{default_telegram_channel}/{message.id})"
            )
        except praw.exceptions.APIException as e:
            logger.warning("API exception: " + e.message)

            if e.error_type == "RATELIMIT":
                return True

        return False

    def _wait_for_rate_limiting_to_pass(self):
        logger.warning(
            f"Waiting {config.getint('general', 'seconds_to_wait_after_rate_limiting')}"
            "seconds for rate-limiting to wear off."
        )
        time.sleep(config.getint("general", "seconds_to_wait_after_rate_limiting"))


def run():
    bot = Bot(utils.reddit_session(), utils.telegram_session())
    
    
    while True:
        try:
            bot.reply_to_username_mentions()
        except Exception as e:
            logger.error(f"Got an unexpected error when reading inbox: {e}")

        time.sleep(config.getint("general", "seconds_between_runs"))
