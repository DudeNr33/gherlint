from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from gherlint.objectmodel import nodes


class GherlintException(Exception):
    """Base class for all custom exceptions issued by Gherlint"""


class InternalError(GherlintException):
    """Intended to be used in places where error handling is necessary e.g. for implementing
    guards to satisfy mypy etc. which should never be reached during normal execution.
    This exception class is never intended to reach the end user."""

    DEFAULT_MESSAGE = (
        "An internal error occured. This should never happen during normal operation, "
        "so if you weren't doing anything fancy, please file a bug report."
    )

    def __init__(self, node: Optional[nodes.Node], message: str = "") -> None:
        super().__init__()
        self.message = (
            self.DEFAULT_MESSAGE + "\n" + message if message else self.DEFAULT_MESSAGE
        )
        if node:
            self.message += (
                f" The error occured when processing the following node: {node}"
            )

    def __str__(self) -> str:
        return self.message


class DuplicateMessageError(GherlintException):
    """Raised if a message is already registered or either the id or name already exists."""


class UnknownMessageError(GherlintException):
    """Raised if an unknown message was requested from the MessageStore"""


class UnsupportedFiletype(GherlintException):
    """Raised if a file with unsupported extension should be processed."""
