# pylint: disable=too-few-public-methods
from gherlint.checkers.base_checker import BaseChecker
from gherlint.registry import CheckerRegistry


class MultiChecker1(BaseChecker):
    pass


class MultiChecker2(BaseChecker):
    pass


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(MultiChecker1)
    registry.register(MultiChecker2)
