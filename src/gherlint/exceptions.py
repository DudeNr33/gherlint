class GherlintException(Exception):
    """Base class for all custom exceptions issued by Gherlint"""


class DuplicateMessageError(GherlintException):
    """Raised if a message is already registered or either the id or name already exists."""


class UnknownMessageError(GherlintException):
    """Raised if an unknown message was requested from the MessageStore"""


class UnsupportedFiletype(GherlintException):
    """Raised if a file with unsupported extension should be processed."""
