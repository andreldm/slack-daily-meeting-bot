from .answer_handler import AnswerHandler
from .cancel_handler import CancelHandler
from .help_handler import HelpHandler
from .start_handler import StartHandler
from .nonsense_handler import NonsenseHandler

class HandlerManager:
    def __init__(self, post, post_report):
        answerHandler = AnswerHandler(post, post_report)

        self.handlers = [
            CancelHandler(post),
            answerHandler,
            StartHandler(post, answerHandler.ask_question),
            HelpHandler(post),
            NonsenseHandler(post)
        ]

    def handle(self, channel, user, msg):
        for h in self.handlers:
            if h.handle(channel, user, msg):
                break

