class CancelHandler:
    def __init__(self, post):
        self.post = post

    def handle(self, channel, user, msg):
        if not msg == 'cancel':
            return False

        if 'current_question' in user and user['current_question'] is not None:
            self.post(channel, "Okay, never mind.")
            del user['current_question']
        else:
            self.post(channel, "You're not reporting.")

        return True

