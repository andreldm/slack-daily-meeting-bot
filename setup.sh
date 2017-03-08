#!/bin/sh

echo "Setting up..."

init_pip=false

if [ ! -d "env" ]; then
    init_pip=true
    virtualenv env
fi

source env/bin/activate

if [ "$init_pip" = true ]; then
    pip install -r requirements.txt
fi

export SLACK_BOT_TOKEN='xoxb-############-########################'

echo "\033[0;32mNow run: python bot.py"
