import pathlib
from os import PathLike
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    # mypy/issues/5667
    StrPathLike = Union[str, PathLike[str]]
else:
    StrPathLike = Union[str, PathLike]


StrPath = Optional[Union[str, pathlib.Path]]
