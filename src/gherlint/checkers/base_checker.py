import inspect
from typing import List, Optional, Type

from gherlint.options import Options
from gherlint.reporting import Message, MessageStore, Reporter


class BaseChecker:
    """Base class for all checkers."""

    MESSAGES: List[Message] = []
    options: Optional[Options] = None

    def __init__(self, reporter: Reporter) -> None:
        self.reporter = reporter
        for message in self.MESSAGES:
            MessageStore().register_message(message)
        self._init_options()

    def _init_options(self) -> None:
        options_class = self.get_options_class()
        if options_class is not None:
            self.options = options_class.from_config()

    @classmethod
    def get_options_class(cls) -> Optional[Type[Options]]:
        annotations = getattr(cls, "__annotations__", {})
        options_class: Optional[Type[Options]] = annotations.get("options")
        if options_class is not None and inspect.isclass(options_class):
            if not issubclass(options_class, Options):
                raise TypeError(
                    "The 'options' attribute of a checker must be a subclass of Options"
                )
            return options_class
        return None
