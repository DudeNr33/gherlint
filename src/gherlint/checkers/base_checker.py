# pylint: disable=too-few-public-methods
from typing import List

from gherlint.reporting import Message, MessageStore, Reporter


class BaseChecker:
    """Base class for all checkers."""

    MESSAGES: List[Message] = []

    def __init__(self, reporter: Reporter):
        self.reporter = reporter
        for message in self.MESSAGES:
            MessageStore().register_message(message)
