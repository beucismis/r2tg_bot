import os
import time
from . import utils
from . import logger
import praw.exceptions
from praw.models import Comment


config = utils.get_config()
logger = logger.get_logger(__name__)
path = os.path.dirname(os.path.abspath(__file__))


class Bot:
    def __init__(self, reddit_session, telegram_session):
        self.reddit_session = reddit_session
        self.telegram_session = telegram_session
        self.inbox = reddit_session.inbox

        self.good_bot_strings = ["good bot", "iyi bot", "cici bot"]
        self.bad_bot_strings = ["bad bot", "kötü bot"]

    def reply_to_username_mentions(self):
        skip = False
        limit_on_inbox = config.getint("general", "limit_on_inbox")

        if not len(self.inbox.unread(limit=limit_on_inbox)):
            skip = True

        if not skip:
            logger.info("Reading inbox...")

        for mention in self.inbox.unread(limit=limit_on_inbox):
            lower = mention.body.lower()

            if isinstance(mention, Comment) and self._was_tagged_in(mention):
                try:
                    self._reply_to_comment(mention)
                except Exception as e:
                    logger.error(f"'{type(e).__name__}': {e}")

            elif lower in self.good_bot_strings:
                self.inbox.mark_read([mention])
                mention.reply("ヽ(•‿•)ノ")
                logger.info(f"u/{utils.author_name(comment)} said good bot.")

            elif lower in self.bad_bot_strings:
                self.inbox.mark_read([mention])
                mention.reply("( ._.)")
                logger.info(f"u/{utils.author_name(comment)} said bad bot.")

        if not skip:
            logger.info("Finished reading inbox.")
            logger.info("-" * 50)

    def _was_tagged_in(self, mention):
        me = self.reddit_session.user.me()

        return f"u/{me.name.lower()}" in mention.body.lower()

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
            if utils.author_name(comment) == utils.author_name(
                mention
            ) and self._was_tagged_in(comment):
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
        filename = submission.url.split("/")[-1]

        video_url = media["reddit_video"]["fallback_url"]
        audio_url = (
            f"{video_url.split('DASH')[0]}DASH_audio.mp4?{video_url.split('?')[-1]}"
        )

        video_path = os.path.join(path, "media", f"{filename}_video.mp4")
        audio_path = os.path.join(path, "media", f"{filename}_audio.mp4")
        output_path = os.path.join(path, "media", f"{filename}.mp4")

        logger.info("Downloading video...")
        utils.download(video_url, video_path)

        try:
            logger.info("Downloading audio...")
            utils.download(audio_url, audio_path)
        except:
            is_audio = False
            os.rename(video_path, output_path)
            logger.info("Downloading audio... Skip.")

        if is_audio:
            logger.info("Merged...")
            utils.merge(video_path, audio_path, output_path)

        logger.info("Uploading video...")
        default_telegram_channel = config.get("general", "default_telegram_channel")

        with self.telegram_session:
            message = self.telegram_session.send_video(
                video=output_path,
                chat_id=config.get("general", "default_telegram_channel"),
                caption=(
                    f"{submission.title}\n\n"
                    f"**Author:** u/#{submission.author}\n"
                    f"**Subreddit:** r/#{submission.subreddit}\n"
                    f"**Link:** {submission.url}"
                ),
            )

        logger.info("Done.")
        logger.info("-" * 50)

        try:
            mention.reply(
                "Yes, video. I'm ready, sending to Telegram...\n\n"
                f"### [Upload via {default_telegram_channel}]"
                f"(https://t.me/s/{default_telegram_channel}/{message.message_id})\n\n"
                f"[About]({config.get('info', 'about')}) | "
                f"[Feedback]({config.get('info', 'feedback')}) | "
                f"[Source Code]({config.get('info', 'source_code')})"
            )
        except praw.exceptions.APIException as e:
            logger.warning("API exception: " + e.message)

            if e.error_type == "RATELIMIT":
                return True

        return False

    def _wait_for_rate_limiting_to_pass(self):
        logger.warning(
            f"Waiting {config.getint('general', 'seconds_to_wait_after_rate_limiting')} "
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
