class CancelHandler:
    def __init__(self, post):
        self.post = post

    def handle(self, event):
        user = event['user']
        channel = event['channel']
        text = event['text']

        if not text.lower() == 'cancel':
            return False

        if 'current_question' in user and user['current_question'] is not None:
            self.post(channel, "Okay, never mind.")
            user['current_question'] = None
        else:
            self.post(channel, "You're not reporting.")

        return True
