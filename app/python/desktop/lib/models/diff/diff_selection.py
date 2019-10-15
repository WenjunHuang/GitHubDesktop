from dataclasses import dataclass
from enum import Enum
from typing import Set, Optional
import itertools


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
        else:
            raise Exception(f'Unknown base selection type {self.default_selection_type}')

    def is_selectable(self, line_index: int) -> bool:
        return (line_index in self.selectable_lines) if self.selectable_lines else True

    def with_line_selection(self, line_index: int, selected: bool) -> 'DiffSelection':
        return self.with_range_selection(line_index, 1, selected)

    def with_range_selection(self, begin: int, length: int, selected: bool) -> 'DiffSelection':
        computed_selection_type = self.get_selection_type()
        to = begin + length

        if type_matches_selection(computed_selection_type, selected):
            return self

        if computed_selection_type == DiffSelectionType.Partial:
            new_diverging_lines = set(self.diverging_lines)

            if type_matches_selection(self.default_selection_type, selected):
                for i in range(begin, to):
                    new_diverging_lines.remove(i)
            else:
                for i in range(begin, to):
                    if self.is_selectable(i):
                        new_diverging_lines.add(i)
            return DiffSelection(
                default_selection_type=self.default_selection_type,
                diverging_lines=None if len(new_diverging_lines) == 0 else new_diverging_lines,
                selectable_lines=self.selectable_lines
            )
        else:
            new_diverging_lines = set(self.diverging_lines)
            for i in range(begin, to):
                if self.is_selectable(i):
                    new_diverging_lines.add(i)

            return DiffSelection(
                default_selection_type=computed_selection_type,
                diverging_lines=new_diverging_lines,
                selectable_lines=self.selectable_lines
            )

    def with_toggle_line_selection(self, line_index: int) -> 'DiffSelection':
        return self.with_line_selection(line_index, not self.is_selected(line_index))

    def with_select_all(self) -> 'DiffSelection':
        return DiffSelection(
            default_selection_type=DiffSelectionType.All,
            diverging_lines=None,
            selectable_lines=set(self.selectable_lines)
        )

    def with_select_none(self) -> 'DiffSelection':
        return DiffSelection(
            default_selection_type=DiffSelectionType.None_,
            diverging_lines=None,
            selectable_lines=set(self.selectable_lines)
        )

    def with_selectable_lines(self, selectable_line: Set[int])->'DiffSelection':
        diverging_lines = set(
            itertools.takewhile(lambda i: i in selectable_line, self.diverging_lines)) if self.diverging_lines else None
        return DiffSelection(
            default_selection_type=self.default_selection_type,
            diverging_lines=diverging_lines,
            selectable_lines=self.selectable_lines
        )


def type_matches_selection(selection_type: DiffSelectionType,
                           selected: bool) -> bool:
    if selection_type == DiffSelectionType.All:
        return selected
    elif selection_type == DiffSelectionType.None_:
        return not selected
    elif selection_type == DiffSelectionType.Partial:
        return False
    else:
        raise Exception(f"Unknown selection type {selection_type}")
