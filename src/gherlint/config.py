from __future__ import annotations

from collections import UserDict
from pathlib import Path
from typing import Optional

import tomli


class Config(UserDict):
    _config: Optional[Config] = None

    def __init__(self, config_file: Path = None, search_path=Path(".")) -> None:
        self._search_path = search_path
        self.config_file = config_file
        config_data = self._load_config_data()
        super().__init__(config_data)

    def _load_config_data(self) -> dict:
        gherlint_toml = self._search_path / "gherlint.toml"
        pyproject_toml = self._search_path / "pyproject.toml"
        if self.config_file:
            data = tomli.loads(self.config_file.read_text("utf8"))
        elif gherlint_toml.exists():
            data = tomli.loads(gherlint_toml.read_text("utf8"))
        elif pyproject_toml.exists():
            data = tomli.loads(pyproject_toml.read_text("utf8"))
            data = data.get("tool", {}).get("gherlint", {})
        else:
            data = {}
        return data

    @classmethod
    def get_config(cls, config_file: Path = None) -> Config:
        """Factory method to access the global config."""
        if not cls._config:
            cls._config = Config(config_file=config_file)
        return cls._config
