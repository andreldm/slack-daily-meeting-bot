# Daily Meeting Bot

A simple bot for daily meetings.

## Requeriments

* Python 3.4+

## Setup

* Set SLACK_BOT_TOKEN in setup.sh (you may find @ api.slack.com/apps/\<APP_ID\>/oauth)

## Running
* `source ./setup.sh`
* `python bot.py`

## Development TODO

* [ ] Add `register` command or something else to register new users
* [ ] Use threading.Timer to randomize report time, set them apart 5 minutes
* [ ] Add `ignore me for # days` command
* [ ] Add `stats` command to display report rates for each user
* [ ] Improve help output
