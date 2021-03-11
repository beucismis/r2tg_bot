# -*- coding: utf-8 -*-
#!/usr/bin/python3


"""
Copyright (C) 2021- beucismis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import click
import subprocess

import config as c


__version__ = "0.1.0"
__author__ = "Adil Gurbuz"
__contact__ = "beucismis@tutamail.com"
__source__ = "https://github.com/beucismis/r2tg_bot"
__description__ = "Uploads Reddit videos to Telegram"


@click.version_option(version=__version__)
@click.option("--run", is_flag=True, help="Run the bot.")
@click.option("--clearallmedia", is_flag=True, help="Clear all media and exit.")
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(run, clearallmedia):
    if run:
        from bot import run_the_bot

        click.echo("Running...")
        run_the_bot()

    if clearallmedia:
        subprocess.run([f"rm -rf {c.MEDIA_PATH}/*.mp4"], shell=True)


if __name__ == "__main__":
    main()
