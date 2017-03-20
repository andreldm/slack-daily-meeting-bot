from datetime import date, datetime

import config

class AnswerHandler:
    def __init__(self, post, post_report):
        self.post = post
        self.post_report = post_report

    def handle(self, channel, user, msg):
        if not 'current_question' in user or user['current_question'] is None:
            return False

        question_id = user['current_question']

        if msg.lower() in ['nothing', 'none', 'nope', 'skip']:
            user['answer{0}'.format(question_id)] = None
            user['current_question'] = question_id + 1
        else:
            user['answer{0}'.format(question_id)] = msg

        if question_id + 1 >= len(config.QUESTIONS):
            self.finish_report(channel, user)
            return True

        question_id += 1
        user['current_question'] = question_id
        self.ask_question(channel, question_id)

        return True

    def ask_question(self, channel, question_id):
        question = config.QUESTIONS[question_id]['text']
        self.post(channel, question)

    def finish_report(self, channel, user):
        title, attachments = self.format_attachments(user)
        user['current_question'] = None
        user['last_report'] = datetime.today()
        if len(attachments) == 0:
            self.post(channel, "I get it, you're not in the mood today.")
            return
        self.post(channel, "Thanks, keep rocking!")
        self.post_report(user, title, attachments)

    def format_attachments(self, user):
        today = date.today().strftime('%b %d, %Y')
        attachments = []
        attachment = {}
        title = "*{0}* posted a status update for *{1}*".format(
            user.get('real_name', user['name']), today)

        for i in range(len(config.QUESTIONS)):
            key = 'answer{0}'.format(i)
            answer = user[key]
            if answer:
                attachment['text'] = "*{0}*\n{1}".format(config.QUESTIONS[i]['text'], answer)
                attachment['color'] = config.QUESTIONS[i]['color']
                attachment['mrkdwn_in'] = ["text"]
                attachments.append(attachment)
                attachment = {}
            user[key] = None

        return title, attachments
