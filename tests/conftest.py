import pytest

from gherlint.reporting import MessageStore


@pytest.fixture(autouse=True)
def clear_messagestore():
    """Clearing the message store is necessary because checker classes will be instantiated multiple times during
    testing in the same python process."""
    MessageStore().clear()
