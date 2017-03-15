import os
import re
import time
import json
import schedule

import config

from slackclient import SlackClient
from handlers import HandlerManager
from storage import Storage

BOT_ID = ''

sc = SlackClient(os.environ['SLACK_BOT_TOKEN'])
storage = Storage()

def post(channel, text, as_user=None):
    if as_user is None:
        as_user = True
    sc.api_call("chat.postMessage", channel=channel, as_user=as_user, text=text)


def post_report(user, title, attachments):
    sc.api_call("chat.postMessage",
                channel=config.DAILY_MEETING_CHANNEL,
                as_user=False,
                username=user['name'],
                icon_url=user['profile']['image_48'],
                text=title,
                attachments=json.dumps(attachments))


handler = HandlerManager(post, post_report)


# http://stackoverflow.com/a/42013042/3109776
def is_direct_message(output, own_id):
    return output and \
        'text' in output and \
        'channel' in output and \
        'type' in output and \
        'user' in output and \
        output['user'] != own_id and \
        output['type'] == 'message' and \
        output['channel'].startswith('D')


def fetch_messages():
    try:
        messages = sc.rtm_read()
        if messages and len(messages) > 0:
            for m in messages:
                handle_message(m)
    except TimeoutError:
        pass


def handle_message(m):
    if not is_direct_message(m, BOT_ID):
        return

    text, user_id, channel = m['text'], m['channel'], m['user']

    if text and channel and user_id:
        user = get_user(user_id)
        handler.handle(channel, user, text)
        storage.save_user(user)


"""Get the user cached in local storage or fetch from API (It'll be cached later)"""
def get_user(user_id):
    user = storage.get_user(user_id, None)
    # TODO: update this user from API once in while
    if user:
        return user
    return sc.api_call("users.info", user=user_id)['user']


def resolve_bot_id():
    res = sc.api_call("users.list")
    if res.get('ok'):
        users = res.get('members')
        for user in users:
            if 'name' in user and user.get('name') == config.BOT_NAME:
                return user.get('id')

    raise Exception("Failed to find bot named '{}'!".format(config.BOT_NAME))

def run_daily_meeting():
    users = storage.get_users_for_daily_meeting()
    print("Run daily meeting:")
    for user in users:
        print(user['name'])
        channel = "@{}".format(user['name'])
        first_name = re.split(" +", user['real_name'])[0].strip()
        post(channel,
             "Hi {}! Time for the standup metting. Please answer the following questions:"
             .format(first_name))
        handler.handle(channel, user, 'report')
        storage.save_user(user)

if __name__ == "__main__":
    if not sc.rtm_connect():
        raise Exception("Connection failed! Please check your Slack Token")

    BOT_ID = resolve_bot_id()
    print("Bot {} connected and running!".format(BOT_ID))

    schedule \
        .every().day \
        .at(config.TIME) \
        .do(run_daily_meeting)

    while True:
        fetch_messages()
        schedule.run_pending()
        time.sleep(1)
