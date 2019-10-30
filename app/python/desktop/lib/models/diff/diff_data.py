from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Union, Iterable, Optional

from typing_extensions import Literal

from desktop.lib.models.diff import DiffHunk, Image


class DiffType(IntEnum):
    Text = auto()
    Image = auto()
    Binary = auto()
    Submodule = auto()
    LargeText = auto()
    Unrenderable = auto()


LineEnding = Union[Literal['CR'], Literal['LF'], Literal['CRLF']]


@dataclass
class LineEndingsChange:
    from_: LineEnding
    to: LineEnding


@dataclass
class TextDiff:
    text: str
    hunks: Iterable[DiffHunk]
    line_endings_change: Optional[LineEndingsChange]
    kind: Literal[DiffType.Text] = field(default=DiffType.Text, init=False)


class ImageDiff:
    previous: Optional[Image]
    current: Optional[Image]
    kind: Literal[DiffType.Image] = field(default=DiffType.Image, init=False)


class BinaryDiff:
    kind: Literal[DiffType.Binary] = field(default=DiffType.Binary, init=False)


class LargeTextDiff:
    text: str
    hunks: Iterable[DiffHunk]
    line_endings_change: Optional[LineEndingsChange]
    kind: Literal[DiffType.LargeText] = field(default=DiffType.LargeText, init=False)

class UnrenderableDiff:
    kind: Literal[DiffType.Unrenderable] = field(default=DiffType.Unrenderable, init=False)



Diff = Union[TextDiff, ImageDiff, BinaryDiff, LargeTextDiff, UnrenderableDiff]
