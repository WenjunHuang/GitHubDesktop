from dataclasses import dataclass
from typing import Iterable, Optional

from desktop.lib.models.author import Author
from desktop.lib.models.changes_selection import ChangesSelection
from desktop.lib.models.commit_message import CommitMessage
from desktop.lib.models.conflict_state import ConflictState
from desktop.lib.models.stash_entry import StashEntry
from desktop.lib.models.working_directory_status import WorkingDirectoryStatus


@dataclass
class ChangesState:
    working_directory: WorkingDirectoryStatus
    # The commit message for a work-in-progress commit in the changes view
    commit_message: CommitMessage

    # Whether or not to show a field for adding co-authors to
    # a commit (currently only supported for GitHub repositories)
    show_coauthor_by: bool

    coauthors: Iterable[Author]

    conflict_state: Optional[ConflictState]

    stash_entry: Optional[StashEntry]

    selection: ChangesSelection
    current_branch_protected: bool
