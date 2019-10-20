from collections import Mapping

from desktop.lib.git.rev_list import rev_symmetric_difference
from desktop.lib.models.branch import AheadBehind


class ComparisonCache:
    def __init__(self):
        self._backing_store: Mapping[str, AheadBehind] = dict()

    def set(self, from_: str, to: str, value: AheadBehind):
        key = rev_symmetric_difference(from_, to)
        self._backing_store[key] = value

    def get(self, from_: str, to: str):
        key = rev_symmetric_difference(from_, to)
        return self._backing_store.get(key)

    def has(self, from_: str, to: str):
        key = rev_symmetric_difference(from_, to)
        return key in self._backing_store.keys()

    def __len__(self):
        return len(self._backing_store)

    def clear(self):
        self._backing_store.clear()
