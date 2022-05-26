"""Common utilities for Sphinx extension scripts."""

from typing import List


class TableWriter:
    def __init__(self) -> None:
        self._lines: List[str] = []

    def add_directive(self) -> None:
        self._lines.append(".. list-table::")
        self._lines.append("   :header-rows: 1")
        self._lines.append("")

    def add_header(self, *headings: str) -> None:
        self.add_row(*headings)

    def add_row(self, *values: str) -> None:
        first = True
        for value in values:
            if first:
                content = f"   * - {value}"
                first = False
            else:
                content = f"     - {value}"
            self._lines.append(content)

    def __str__(self) -> str:
        return "\n".join(self._lines) + "\n\n"
