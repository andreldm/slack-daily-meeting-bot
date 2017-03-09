class HelpHandler:
    def __init__(self, post):
        self.post = post

    def handle(self, channel, user, msg):
        if msg == 'help':
            self.post(channel, """This is what I can do for you:
`report` Start a daily meeting report manually""")
            return True

        return False

