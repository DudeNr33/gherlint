# pylint: disable=too-few-public-methods
from gherlint.checkers.base_checker import BaseChecker
from gherlint.registry import CheckerRegistry


class SingleDummyChecker(BaseChecker):
    pass


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(SingleDummyChecker)
