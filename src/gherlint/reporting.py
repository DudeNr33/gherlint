import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from gherlint.exceptions import DuplicateMessageError, UnknownMessageError
from gherlint.objectmodel.nodes import Document, Node


@dataclass(frozen=True)
class Message:
    id: str  # ID, like E001  pylint: disable=invalid-name
    name: str  # unique short name, like missing-feature-name
    text: str  # More detailed textual description of the problem and optionally a hint how to solve the problem.

    id_pattern = re.compile(r"^[EWCR]\d{3}$")
    name_pattern = re.compile(r"^[a-zA-Z]+(-[a-zA-Z]+)*$")

    def __post_init__(self):
        if not self.id_pattern.match(self.id):
            raise ValueError(f"Value for id must conform to {self.id_pattern.pattern}")
        if not self.name_pattern.match(self.name):
            raise ValueError(
                f"Value for name must conform to {self.name_pattern.pattern}"
            )


class MessageStore:
    id_to_message: Dict[str, Message] = {}
    name_to_message: Dict[str, Message] = {}

    @classmethod
    def register_message(cls, message: Message) -> None:
        if message.id in cls.id_to_message:
            raise DuplicateMessageError(
                f"Message with ID {message.id} already registered"
            )
        if message.name in cls.name_to_message:
            raise DuplicateMessageError(
                f"Message with name {message.name} already registered"
            )
        cls.id_to_message[message.id] = message
        cls.name_to_message[message.name] = message

    @classmethod
    def clear(cls):
        cls.id_to_message.clear()
        cls.name_to_message.clear()

    @classmethod
    def get_by_id(cls, message_id: str):
        try:
            return cls.id_to_message[message_id]
        except KeyError as exc:
            raise UnknownMessageError(f"Message ID {message_id} not found.") from exc

    @classmethod
    def get_by_name(cls, name: str):
        try:
            return cls.name_to_message[name]
        except KeyError as exc:
            raise UnknownMessageError(f"Message name '{name}' not found.") from exc


class Reporter(ABC):
    """Base class for reporters."""

    def add_message(self, id_or_name: str, node: Node, **format_args) -> None:
        """Add a message, identified by its id or name, that shall be emitted"""
        if Message.id_pattern.match(id_or_name):
            message = MessageStore.get_by_id(id_or_name)
        elif Message.name_pattern.match(id_or_name):
            message = MessageStore.get_by_name(id_or_name)
        else:
            raise ValueError(
                f"{id_or_name} matches neither the pattern for a message ID nor a message name."
            )
        self.emit(message, node, **format_args)

    @abstractmethod
    def emit(self, message: Message, node: Node, **format_args) -> None:
        """Emit the message as it is suitable for the desired report format"""


class TextReporter(Reporter):
    """Simple text based reporter that prints to stdout"""

    # example: missing_feature_name.feature:1:0: Feature has no name (missing-feature-name)
    MSG_TEMPLATE = "{file}:{line}:{column}: {text} ({name})"

    def __init__(self):
        self.current_file = None

    def emit(self, message: Message, node: Node, **format_args) -> None:
        root = node.get_root()
        if not isinstance(root, Document):
            raise RuntimeError(
                "The node passed to add_message does not have a root parent of type Document."
                "This should never happen if gherlint is used from the command line."
            )
        file = root.filename
        if file != self.current_file:
            self.current_file = file
            self.new_section_for_file()
        msg_text = message.text.format(**format_args) if format_args else message.text
        print(
            self.MSG_TEMPLATE.format(
                file=file,
                line=node.line,
                column=node.column,
                text=msg_text,
                name=message.name,
            )
        )

    def new_section_for_file(self):
        print(f"************* {self.current_file}")
