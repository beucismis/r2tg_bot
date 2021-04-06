# r2tg_bot

<img src="assets/screenshot.png" width="400" align="right">

![](https://img.shields.io/badge/r2tg__bot-ONLINE-green) ![](https://img.shields.io/pypi/v/r2tg_bot) ![](https://img.shields.io/pypi/l/r2tg_bot) ![](https://img.shields.io/badge/style-black-black?style=flat)

Easiest way to upload Reddit videos to Telegram. Just comment bots nickname...

Reddit bot: [reddit.com/u/r2tg_bot](https://reddit.com/u/r2tg_bot) ![](https://img.shields.io/reddit/user-karma/combined/r2tg_bot) <br/>
Telegram bot: [t.me/r2tg_bot](https://t.me/r2tg_bot) <br/>
Telegram archive channel: [t.me/s/r2tg_bot_archive](https://t.me/s/r2tg_bot_archive)

### Availability
Only GNU/Linux 🐧

## Dependencies
* Python 3
* [praw](https://github.com/praw-dev/praw)
* [tgcrypto](https://github.com/pyrogram/tgcrypto)
* [pyrogram](https://github.com/pyrogram/pyrogram)
* [FFmpeg](https://ffmpeg.org)
  * Debian based systems: `apt install ffmpeg` <br/>
  * Arch based system: `pacman -S ffmpeg4.0`

## Building and Installation

### Building the sources
1. Clone the reporistrory: 
```sh
$ git clone https://github.com/beucismis/r2tg_bot
$ cd r2tg_bot/
```
2. Install r2tg_bot dependencies:
```sh
$ pip3 install -r requirements.txt
```
4. Edit `praw.ini` and `pyrogram.ini` files.
5. Run bot:
```sh
$ chmod u+x run.sh
$ ./run.sh
```

## Donation
Soon...

## Lisance
This project lisanced under GPL-3.0 - for details check [LICENSE](LICENSE) file.
