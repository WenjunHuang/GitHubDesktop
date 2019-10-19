from dataclasses import dataclass


@dataclass
class RepositoryState:
    commit_selection:CommitSelection
    changes_state:ChangesState
    compare_state:CompareState
    commit_author:CommitIdentity
