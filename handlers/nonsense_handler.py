class NonsenseHandler:
    def __init__(self, post):
        self.post = post

    def handle(self, channel, user, msg):
        self.post(channel, """Sorry, I didn't get that :pensive:.
Type `help` and I'll explain what I can do.""")

        return True

