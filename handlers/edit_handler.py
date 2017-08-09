from datetime import date, datetime

import config


def format_attachments(user):
    today = date.today().strftime('%b %d, %Y')
    attachments = []
    attachment = {}
    title = "*{0}* posted a status update for *{1}* (edited)".format(
        user.get('real_name') or user.get('name'), today)

    for i in range(len(config.QUESTIONS)):
        key = 'previous_answer{0}'.format(i)
        answer = user[key]
        if answer:
            attachment['text'] = "*{0}*\n{1}".format(config.QUESTIONS[i]['text'], answer)
            attachment['color'] = config.QUESTIONS[i]['color']
            attachment['mrkdwn_in'] = ["text"]
            attachments.append(attachment)
            attachment = {}

    return title, attachments


class EditHandler:
    def __init__(self, update_report):
        self.update_report = update_report

    def handle(self, event):
        text = event['text']
        user = event['user']
        channel = event['channel']
        msg = event['msg']

        if 'previous_message' not in msg or msg['previous_message'] is None:
            return False

        if 'current_question' in user and user['current_question']:
            # TODO Update user answer during report
            return True

        previous_text = msg['previous_message']['text']
        print(previous_text)

        for i in range(len(config.QUESTIONS)):
            key = 'previous_answer{0}'.format(i)
            if user[key] == previous_text:
                user[key] = text

        title, attachments = format_attachments(user)
        self.update_report(user, user['last_report_channel'], title, attachments, user['last_report_ts'])

        return True
