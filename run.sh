#!/bin/bash

BASEDIR=$(dirname "$0")

cd $BASEDIR/r2tg_bot/
/usr/bin/python3 __init__.py --run
