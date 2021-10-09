from typing import NamedTuple, Protocol

from gherlint.objectmodel.nodes import Document, Node


class Message(NamedTuple):
    id: str
    text: str


class Reporter(Protocol):
    """This class defines the protocol which a concrete reporter class must adhere to."""

    def add_message(self, message: Message, node: Node) -> None:
        """Add a message that shall be emitted"""


class TextReporter:
    """Simple text based reporter that prints to stdout"""

    # example: missing_feature_name.feature:1:0: Feature has no name (missing-feature-name)
    MSG_TEMPLATE = "{file}:{line}:{column}: {text} ({msgid})"

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
                msgid=message.id,
            )
        )

    def new_section_for_file(self):
        print(f"************* {self.current_file}")
