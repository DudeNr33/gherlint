from pathlib import Path
from typing import Iterator, Union

from gherlint.exceptions import UnsupportedFiletype


def iter_feature_files(path: Union[str, Path]) -> Iterator[Path]:
    if isinstance(path, str):
        path = Path(path)
    if path.is_file():
        if path.suffix == "feature":
            yield path
        else:
            raise UnsupportedFiletype(f"{path} is not a .feature file.")
    else:
        yield from path.rglob("*.feature")
