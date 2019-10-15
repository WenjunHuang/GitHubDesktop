from dataclasses import dataclass
from enum import Enum
from typing import Set, Optional


class DiffSelectionType(Enum):
    All = 'All'
    Partial = 'Partial'
    None_ = 'None'


@dataclass
class DiffSelection:
    default_selection_type: DiffSelectionType
    diverging_lines: Optional[Set[int]] = None
    selectable_lines: Optional[Set[int]] = None

    def get_selection_type(self) -> DiffSelectionType:
        if not self.diverging_lines:
            return self.default_selection_type

        if self.selectable_lines and len(self.selectable_lines) == len(self.diverging_lines):
            all_selectable_lines_are_divergent = all(i in self.diverging_lines for i in self.selectable_lines)

            if all_selectable_lines_are_divergent:
                return DiffSelectionType.None_ if self.default_selection_type == DiffSelectionType.All else DiffSelectionType.All

        return DiffSelectionType.Partial

    def is_selected(self, line_index: int) -> bool:
        line_is_divergent = self.diverging_lines and (line_index in self.diverging_lines)

        if self.default_selection_type == DiffSelectionType.All:
            return not line_is_divergent
        elif self.default_selection_type == DiffSelectionType.None_:
            return bool(line_is_divergent)

    def is_selectable(self,line_index:int)->bool:
        return (line_index in self.selectable_lines) if self.selectable_lines else True
