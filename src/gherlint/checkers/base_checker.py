# pylint: disable=too-few-public-methods
from typing import List, Optional, Type

from gherlint.options import Options
from gherlint.reporting import Message, MessageStore, Reporter


class BaseChecker:
    """Base class for all checkers."""

    MESSAGES: List[Message] = []
    has_options = False
    options: Optional[Options] = None

    def __init__(self, reporter: Reporter) -> None:
        self.reporter = reporter
        for message in self.MESSAGES:
            MessageStore().register_message(message)
        if self.has_options:
            self._init_options()

    def _init_options(self) -> None:
        annotations = getattr(self, "__annotations__", {})
        options_class: Optional[Type[Options]] = annotations.get("options")
        if options_class is not None:
            self.options = options_class.from_config()
