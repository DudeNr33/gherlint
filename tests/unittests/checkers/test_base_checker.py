from gherlint.checkers.base_checker import BaseChecker
from gherlint.reporting import Message, MessageStore


class MyChecker(BaseChecker):  # pylint: disable=too-few-public-methods
    MESSAGES = [
        Message("C001", "first-message", ""),
        Message("C002", "second-message", ""),
        Message("C003", "third-message", ""),
    ]


class TestBaseChecker:
    @staticmethod
    def test_base_class_registers_messages():
        checker = MyChecker(reporter=None)
        assert all(
            msg in MessageStore().id_to_message.values() for msg in checker.MESSAGES
        )
