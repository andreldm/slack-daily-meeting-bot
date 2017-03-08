import os
import time
import datetime
import json
from slackclient import SlackClient

BOT_ID = ''
BOT_NAME = 'dailymeetingbot'
DAILY_MEETING_CHANNEL = 'G4FG6LYKZ'

COMMAND_ECHO = 'echo'
COMMAND_HELP = 'help'

sc = SlackClient(os.environ['SLACK_BOT_TOKEN'])

def print_help(channel):
    sc.api_call("chat.postMessage", channel=channel, as_user=True,
                text="""This is what I can do for you:
`echo` I'll repeat what you say in the daily meeting channel
""")

# http://stackoverflow.com/a/42013042/3109776
def is_direct_message(output):
    return output and \
        'text' in output and \
        'channel' in output and \
        'type' in output and \
        'user' in output and \
        output['user'] != BOT_ID and \
        output['type'] == 'message' and \
        output['channel'].startswith('D')


def format_message(user, msg):
    today = datetime.date.today().strftime('%b %d, %Y')

    return [{
        'pretext': "*{0}* posted a status update for *{1}*".format(user['real_name'], today),
        'text': "*O que você conseguiu ontem?*\n" + msg,
        'color': '#C0DADB',
        'mrkdwn_in': ["text", "pretext"]
    },{
        'text': "*O que você vai fazer hoje?*\n" + msg,
        'color': '#839BBD',
        'mrkdwn_in': ["text"]
    },{
        'text': "*Quais obstáculos estão impedindo o seu progresso?*\n" + msg,
        'color': '#E59797',
        'mrkdwn_in': ["text"]
    }]

def handle_message(message, channel, user_id):
    user = sc.api_call("users.info", user=user_id)['user']

    command = message.split(' ')[0].strip()
    args = message.replace(command, '', 1).strip()
    command = command.lower()

    if command == COMMAND_ECHO:
        sc.api_call("chat.postMessage",
                    channel=DAILY_MEETING_CHANNEL,
                    as_user=False,
                    username=user['name'],
                    icon_url=user['profile']['image_48'],
                    text='',
                    attachments=json.dumps(format_message(user, args)))
        return

    if command == COMMAND_HELP:
        print_help(channel)
        return

    sc.api_call("chat.postMessage", channel=channel, as_user=True,
                text="Sorry, I didn't get that :pensive:. Type `help` and I'll tell you what I can do.")

def parse_slack_output(output_list):
    if output_list and len(output_list) > 0:
        for output in output_list:
            if is_direct_message(output):
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
        command, channel, user = parse_slack_output(sc.rtm_read())
        if command and channel and user:
            handle_message(command, channel, user)
        time.sleep(1)

