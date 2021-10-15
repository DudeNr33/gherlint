import importlib
from pathlib import Path
from typing import Iterable, Iterator, List, Type

from gherlint.checkers.base_checker import BaseChecker

CHECKER_PACKAGE = "checkers"
CHECKER_PATH = Path(__file__).parent / CHECKER_PACKAGE
PREFIX = "gherlint"


class CheckerRegistry(Iterable):
    def __init__(self) -> None:
        self._checkers: List[Type[BaseChecker]] = []

    def discover(self) -> None:
        for modname in CHECKER_PATH.glob("*.py"):
            module = importlib.import_module(
                f"{PREFIX}.{CHECKER_PACKAGE}.{modname.stem}"
            )
            if hasattr(module, "register_checker"):
                module.register_checker(self)  # type: ignore

    def register(self, checker: Type[BaseChecker]) -> None:
        self._checkers.append(checker)

    def __iter__(self) -> Iterator[Type[BaseChecker]]:
        yield from self._checkers
