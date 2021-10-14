import re
import string

import pytest

from gherlint.exceptions import DuplicateMessageError, UnknownMessageError
from gherlint.reporting import Message, MessageStore


class TestMessage:
    ALLOWED_STARTCHARACTERS = ["E", "C", "W", "I"]
    WRONG_STARTCHARACTERS = [
        c for c in string.ascii_letters if c not in ["E", "C", "W", "I"]
    ]

    @staticmethod
    @pytest.mark.parametrize(
        "msg_id, name, text",
        [
            ("C001", "foo", "bar"),
            ("E999", "foo-bar-baz", "This is a longer text"),
            ("C123", "foo", ""),
            ("I000", "foo", ""),
        ],
    )
    def test_create_valid_message_succeeds(msg_id, name, text):
        msg = Message(msg_id, name, text)
        assert msg.id == msg_id
        assert msg.name == name
        assert msg.text == text

    @staticmethod
    @pytest.mark.parametrize(
        "msg_id", [f"{c}000" for c in WRONG_STARTCHARACTERS] + ["Eabc", "E00", "E0000"]
    )
    def test_invalid_id_raises_value_error(msg_id):
        with pytest.raises(
            ValueError,
            match=re.escape(
                f"Value for id must conform to {Message.id_pattern.pattern}"
            ),
        ):
            Message(msg_id, "test", "")


class TestMessageStore:
    messagestore = MessageStore()

    def test_register_new_message_succeeds(self):
        msg = Message(id="C001", name="test-message", text="")
        self.messagestore.register_message(msg)
        assert msg in self.messagestore.id_to_message.values()

    def test_registering_same_message_twice_fails(self):
        msg = Message(id="C001", name="test-message", text="")
        self.messagestore.register_message(msg)
        with pytest.raises(DuplicateMessageError):
            self.messagestore.register_message(msg)
        assert msg in self.messagestore.id_to_message.values()

    def test_registering_message_with_same_id_fails(self):
        first_msg = Message("C001", "same-name", "")
        second_msg = Message("C001", "new-name", "")
        self.messagestore.register_message(first_msg)
        with pytest.raises(
            DuplicateMessageError, match="Message with ID C001 already registered"
        ):
            self.messagestore.register_message(second_msg)

    def test_registering_message_with_same_name_fails(self):
        first_msg = Message("C001", "same-name", "")
        second_msg = Message("C002", "same-name", "")
        self.messagestore.register_message(first_msg)
        with pytest.raises(
            DuplicateMessageError,
            match="Message with name same-name already registered",
        ):
            self.messagestore.register_message(second_msg)

    def test_get_known_message_by_id(self):
        msg = Message("C001", "name", "")
        self.messagestore.register_message(msg)
        retrieved_msg = self.messagestore.get_by_id(msg.id)
        assert retrieved_msg is msg

    def test_get_unknown_message_by_id(self):
        with pytest.raises(UnknownMessageError, match="Message ID C999 not found."):
            self.messagestore.get_by_id("C999")

    def test_get_known_message_by_name(self):
        msg = Message("C001", "name", "")
        self.messagestore.register_message(msg)
        retrieved_msg = self.messagestore.get_by_name(msg.name)
        assert retrieved_msg is msg

    def test_get_unknown_message_by_name(self):
        with pytest.raises(
            UnknownMessageError, match="Message name 'unknown' not found."
        ):
            self.messagestore.get_by_name("unknown")

    @staticmethod
    def test_all_instances_share_same_data():
        msgstore1 = MessageStore()
        msgstore2 = MessageStore()
        msg = Message("C001", "test-message", "")
        msgstore1.register_message(msg)
        assert msgstore1.id_to_message == msgstore2.id_to_message
        assert msgstore1.name_to_message == msgstore2.name_to_message
