# r2tg_bot

![](https://img.shields.io/uptimerobot/status/m790607794-5f03cd33d5ce1319d7b290f6) ![](https://img.shields.io/badge/python-v3.6%2B-blue) ![](https://img.shields.io/github/languages/code-size/beucismis/r2tg_bot) ![](https://img.shields.io/badge/style-black-black)

A Reddit bot that uploads video or GIF files to Telegram. Just mention me (`u/r2tg_bot`) in the comments. All requests are upload to archive channel by default. NSFW etc. content is not allowed on default channel. If you liked me, reply to my answer saying "good bot".

Archive channel: https://t.me/s/r2tg_bot_archive

<details>
  <summary>Show the demo</summary>
  <img src="https://user-images.githubusercontent.com/40023234/153205793-f4ff6f5a-8b1e-4d9c-a432-c981b07ca54b.jpg" width="400">
  <img src="https://user-images.githubusercontent.com/40023234/153206077-987b3dec-1c1a-4bb5-8a2e-247eaca19a6e.png" width="358">
</details>

## Features

- Tiny and fast
- Customizable
- Self-hosted
- Trigger with comment
- Video and GIF upload
- Written in Python

## Requirements

Python: `3.6+` is required. Also it use [FFmpeg](https://ffmpeg.org) to merge downloaded video and audio.

For Debian based: 
```sh
apt install ffmpeg
```
For Arch based: 
```sh
pacman -S ffmpeg4.0
```

## Installing and Running

Clone the reporistrory:
```
git clone https://github.com/beucismis/r2tg_bot
```
Install dependencies:
```
pip3 install --user -r requirements.txt
```
Set service file (Don't forget to set the [user](https://github.com/beucismis/r2tg_bot/blob/main/r2tg_bot.service#L11-L14)):
```
cp r2tg_bot.service /etc/systemd/system/
```
Set configuration file ([Click](#configuration-file) for more):
```
cd src/
cp config.ini.sample config.ini
```
Running the bot:
```
service r2tg_bot enable # or disable
service r2tg_bot start # or restart maybe stop
```
Chech the bot status:
```
service r2tg_bot status
```

## Configuration File

General:
| key | type | description |
| --- | ---- | ----- |
| `limit_on_inbox` | `int` | The number of messages to read in the Reddit inbox. |
| `comment_log_indent` | `int` | ? |
| `seconds_between_runs` | `int` | Cycle waiting time. In seconds. |
| `max_num_tags_per_user_in_chain` | `int` | Max num tags per user in chain. |
| `seconds_to_wait_after_rate_limiting` | `int` | Seconds to wait after rate limiting. |
| `default_telegram_channel` | `str` | Channel name. Don't forget to add the bot to the channel. |

Reddit:
| key | type | description |
| --- | ---- | ----- |
| `username` | `str` | Reddit acount username. E.g: `u/r2tg_bot` |
| `password` | `str` | Reddit acount password. |
| `user_agent` | `str` | Reddit user-agent. E.g: `r2tg_bot by u/beucismis` |
| `client_id` | `str` | Reddit client ID. See: https://old.reddit.com/prefs/apps/ |
| `client_secret` | `str` | Reddit client secret. See: https://old.reddit.com/prefs/apps/ |


Telegram:
| key | type | description |
| --- | ---- | ----- |
| `session_name` | `str` | Session name. E.g: `r2tg_bot` |
| `api_id` | `str` | App ID. See: https://my.telegram.org/apps |
| `api_hash` | `str` | API hash. See: https://my.telegram.org/apps |
| `bot_token` | `str` | Bot token: See: https://core.telegram.org/api#bot-api |

Black List:
| key | type | description |
| --- | ---- | ----- |
| `users` | `str` | Blocked users list. E.g: `AutoModerator,Sub_Corrector_Bot` |
| `subrettis` | `str` | Blocked subreddits list. E.g: `depression,SuicideWatch` |
 
Info:
| key | type | description |
| --- | ---- | ----- |
| `source_code` | `str` | Source code URL. |
| `about` | `str` | About page URL. |
| `feedback` | `str` | Feedback page URL. |

## Tips and Tricks

Use `tail -f src/logs/r2tg_bot.log` for live log output. <br/>
Add `0 0 * * * /bin/rm -f /home/username/r2tg_bot/src/media/*.mp4` to your cron file to clean media once a day.

## License
This project lisanced under GPL-3.0 - for details check [LICENSE](LICENSE) file.
