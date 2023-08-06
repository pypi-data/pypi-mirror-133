import shlex
from typing import Iterable

try:
    shlex_join = shlex.join  # type: ignore[attr-defined]
except AttributeError:

    def shlex_join(split_command: Iterable[str]) -> str:
        return " ".join(shlex.quote(arg) for arg in split_command)


try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore[no-redef]


__all__ = ["version"]
