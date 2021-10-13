import re
from dataclasses import dataclass
from typing import Dict, Protocol

from gherlint.exceptions import DuplicateMessageError, UnknownMessageError
from gherlint.objectmodel.nodes import Document, Node


@dataclass(frozen=True)
class Message:
    id: str  # ID, like E001  pylint: disable=invalid-name
    name: str  # unique short name, like missing-feature-name
    text: str  # More detailed textual description of the problem and optionally a hint how to solve the problem.

    id_pattern = re.compile(r"^[EWCI]\d{3}$")
    name_pattern = re.compile(r"^[a-zA-Z]+(-[a-zA-Z]+)*$")

    def __post_init__(self):
        if not self.id_pattern.match(self.id):
            raise ValueError(f"Value for id must conform to {self.id_pattern.pattern}")
        if not self.name_pattern.match(self.name):
            raise ValueError(
                f"Value for name must conform to {self.name_pattern.pattern}"
            )


class MessageStore:
    def __init__(self):
        self.id_to_message: Dict[str, Message] = {}
        self.name_to_message: Dict[str, Message] = {}

    def register_message(self, message: Message) -> None:
        if message.id in self.id_to_message:
            raise DuplicateMessageError(
                f"Message with ID {message.id} already registered"
            )
        if message.name in self.name_to_message:
            raise DuplicateMessageError(
                f"Message with name {message.name} already registered"
            )
        self.id_to_message[message.id] = message
        self.name_to_message[message.name] = message

    def get_by_id(self, message_id: str):
        try:
            return self.id_to_message[message_id]
        except KeyError as exc:
            raise UnknownMessageError(f"Message ID {message_id} not found.") from exc

    def get_by_name(self, name: str):
        try:
            return self.name_to_message[name]
        except KeyError as exc:
            raise UnknownMessageError(f"Message name '{name}' not found.") from exc


class Reporter(Protocol):
    """This class defines the protocol which a concrete reporter class must adhere to."""

    def add_message(self, message: Message, node: Node) -> None:
        """Add a message that shall be emitted"""


class TextReporter:
    """Simple text based reporter that prints to stdout"""

    # example: missing_feature_name.feature:1:0: Feature has no name (missing-feature-name)
    MSG_TEMPLATE = "{file}:{line}:{column}: {text} ({name})"

    def __init__(self):
        self.current_file = None

    def add_message(self, message: Message, node: Node) -> None:
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
        print(
            self.MSG_TEMPLATE.format(
                file=file,
                line=node.line,
                column=node.column,
                text=message.text,
                name=message.name,
            )
        )

    def new_section_for_file(self):
        print(f"************* {self.current_file}")
