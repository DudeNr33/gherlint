import inspect
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
        self._init_options()

    def _init_options(self) -> None:
        annotations = getattr(self, "__annotations__", {})
        options_class: Optional[Type[Options]] = annotations.get("options")
        if options_class is not None and inspect.isclass(options_class):
            if not issubclass(options_class, Options):
                raise TypeError(
                    "The 'options' attribute of a checker must be a subclass of Options"
                )
            self.options = options_class.from_config()
