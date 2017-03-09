class StartHandler:
    def __init__(self, post, ask_question):
        self.post = post
        self.ask_question = ask_question

    def handle(self, channel, user, msg):
        if msg == 'report':
            if 'current_question' in user and user['current_question']:
                self.post(channel, "Already reporting.")
            else:
                user['current_question'] = 0
                self.ask_question(channel, 0)
            return True

        return False

