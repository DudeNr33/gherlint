# pylint: disable=too-few-public-methods
from gherlint.reporting import Reporter


class BaseChecker:
    """Base class for all checkers."""

    def __init__(self, reporter: Reporter):
        self.reporter = reporter
