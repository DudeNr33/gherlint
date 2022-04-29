"""Options and options handling for checkers of other classes."""
from __future__ import annotations

from gherlint.config import Config


class Options:
    """Options for a checker."""

    config_section: str = "default"

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            annotations = getattr(self, "__annotations__", {})
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise ValueError(
                        f"Invalid type for option '{name}': "
                        f"expected '{expected_type}', got '{type(value)}'"
                    )
                setattr(self, name, value)

    @classmethod
    def from_config(cls) -> Options:
        """Create options from the config."""
        config = Config.get_config()
        options = config.get(cls.config_section, {})
        return cls(**options)
