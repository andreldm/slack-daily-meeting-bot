from util import Util

QUESTIONS = [
    {'text': "O que você conseguiu ontem?", 'color': '#C0DADB' },
    {'text': "O que você vai fazer hoje?", 'color': '#839BBD' },
    {'text': "Quais obstáculos estão impedindo o seu progresso?", 'color': '#E59797' }
]

class MessageHandler:
    def __init__(self, post, post_report):
        self.post = post
        self.post_report = post_report
        self.util = Util()


    def ask_question(self, channel, question):
        self.post(channel, question)
        pass


    def handle_help(self, channel, msg):
        if msg == 'help':
            self.post(channel, """This is what I can do for you:
`report` Start a daily meeting report manually""")
            return True

        return False


    def finish_report(self, channel, user):
        title, attachments = self.util.format_attachments(user, QUESTIONS)
        self.post_report(channel, user, title, attachments)


    def handle_answer(self, channel, user, msg):
        if not 'current_question' in user: return False

        question = user['current_question']

        if msg == 'none':
            user['answer{0}'.format(question)] = None
            user['current_question'] = question + 1
            return True

        if msg == 'cancel':
            self.post(channel, "Okay, never mind.")
            del user['current_question']
            return True

        user['answer{0}'.format(question)] = msg

        if question + 1 >= len(QUESTIONS):
            self.finish_report(channel, user)
            return True

        question = user['current_question'] = question + 1
        self.ask_question(channel, QUESTIONS[question]['text'])
        return True


    def start_report(self, channel, user, msg):
        if msg == 'report':
            user['current_question'] = 0
            self.ask_question(channel, QUESTIONS[0]['text'])
            return True

        return False


    def handle_message(self, channel, user, msg):
        if self.handle_help(channel, msg): return
        if self.handle_answer(channel, user, msg): return
        if self.start_report(channel, user, msg): return

        if msg in ['cancel']:
            self.post(channel, "You're not reporting")
            return

        self.post(channel, """Sorry, I didn't get that :pensive:.
Type `help` and I'll explain what I can do.""")
