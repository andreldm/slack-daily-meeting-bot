import os
import time
import json

from slackclient import SlackClient
from handlers import HandlerManager
from storage import Storage

BOT_ID = ''
BOT_NAME = 'dailymeetingbot'
DAILY_MEETING_CHANNEL = '#test-dailymeetingbot'

COMMAND_ECHO = 'echo'
COMMAND_HELP = 'help'

sc = SlackClient(os.environ['SLACK_BOT_TOKEN'])
storage = Storage()

def post(channel, text, as_user=None):
    if as_user is None: as_user = True
    sc.api_call("chat.postMessage", channel=channel, as_user=as_user, text=text)


def post_report(user, title, attachments):
    sc.api_call("chat.postMessage",
            channel=DAILY_MEETING_CHANNEL,
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


def parse_output(output_list):
    if output_list and len(output_list) > 0:
        for output in output_list:
            if is_direct_message(output, BOT_ID):
                print (output)
                return output['text'], output['channel'], output['user']
    return None, None, None


def resolve_bot_id():
    res = sc.api_call("users.list")
    if res.get('ok'):
        users = res.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')

    raise Exception("Failed to find bot named '{0}'!".format(BOT_NAME))


if __name__ == "__main__":
    if not sc.rtm_connect():
        raise Exception("Connection failed! Please check your Slack Token")

    BOT_ID = resolve_bot_id()
    print("Bot {0} connected and running!".format(BOT_ID))

    while True:
        msg, channel, user_id = parse_output(sc.rtm_read())
        if msg and channel and user_id:
            user = sc.api_call("users.info", user=user_id)['user']
            user = storage.get_user(user['id'], user)
            handler.handle(channel, user, msg)
            storage.save_user(user)
        time.sleep(1)

