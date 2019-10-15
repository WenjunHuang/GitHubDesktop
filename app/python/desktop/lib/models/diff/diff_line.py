from enum import Enum
from dataclasses import dataclass, replace

# indicate what a line in the diff represents
from typing import Optional


class DiffLineType(Enum):
    Context = 'context'
    Add = 'add'
    Delete = 'delete'
    Hunk = ' hunk'


@dataclass
class DiffLine:
    text: str
    type: DiffLineType
    old_line_number: Optional[int]
    new_line_number: Optional[int]
    no_trailing_newline: bool = False

    def with_no_trailing_newline(self, no_trailing_newline: bool) -> 'DiffLine':
        return replace(self, no_trailing_newline=no_trailing_newline)

    def is_includable_line(self):
        return self.type == DiffLineType.Add or self.type==DiffLineType.Delete

    def content(self)->str:
        return self.text[1:]
