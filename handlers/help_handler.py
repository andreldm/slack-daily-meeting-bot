class HelpHandler:
    def __init__(self, post):
        self.post = post

    def handle(self, event):
        if event['text'].lower() == 'help':
            self.post(event['channel'], """This is what I can do for you:
*Commands:*
`report`, `start` Starts a daily meeting report manually
`help` Displays this help message

*During reporting you can also issue:*
`nothing`, `none`, `nope`, `skip` Ignores a question during report
`cancel` Cancels and deletes all the report
""")
            return True

        return False

