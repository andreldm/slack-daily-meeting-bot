from .answer_handler import AnswerHandler
from .cancel_handler import CancelHandler
from .help_handler import HelpHandler
from .start_handler import StartHandler
from .nonsense_handler import NonsenseHandler

class HandlerManager:
    def __init__(self, post, post_report):
        answer_handler = AnswerHandler(post, post_report)

        self.handlers = [
            CancelHandler(post),
            HelpHandler(post),
            StartHandler(post, answer_handler.ask_question),
            answer_handler,
            NonsenseHandler(post)
        ]

    def handle(self, channel, user, msg):
        for handler in self.handlers:
            if handler.handle(channel, user, msg):
                break

