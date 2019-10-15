from dataclasses import dataclass
from typing import List

from .diff_line import DiffLine


@dataclass
class DiffHunkHeader:
    old_start_line: int
    old_line_count: int
    new_start_line: int
    new_line_count: int


@dataclass
class DiffHunk:
    header: DiffHunkHeader
    lines: List[DiffLine]
    unified_diff_start: int
    unified_diff_end: int


@dataclass
class GitRawDiff:
    header:str
    contents:str
    hunks:List[DiffHunk]
    is_binary:bool
