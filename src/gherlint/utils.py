from pathlib import Path
from typing import Iterator, List, Union

from gherkin.dialect import DIALECTS

from gherlint.exceptions import UnsupportedFiletype


def iter_feature_files(path: Union[str, Path]) -> Iterator[Path]:
    if isinstance(path, str):
        path = Path(path)
    if path.is_file():
        if path.suffix == ".feature":
            yield path
        else:
            raise UnsupportedFiletype(f"{path} is not a .feature file.")
    else:
        yield from path.rglob("*.feature")


def get_keyword_candidates(keyword: str) -> List[str]:
    """Get a list of the possible words of the keyword in all languages."""
    candidates = []
    for language in DIALECTS.values():
        candidates.extend(language[keyword])
    return candidates
