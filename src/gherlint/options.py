"""Options and options handling for checkers of other classes."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from gherlint.config import Config


class Options(BaseModel):
    """Options for a checker."""

    config_section: ClassVar[str] = Field(
        ..., description="config section with options for a checker"
    )

    @classmethod
    def from_config(cls) -> Options:
        """Create options from the config."""
        config = Config.get_config()
        options = config.get(cls.config_section, {})  # type: ignore
        return cls(**options)
