from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Mapping, Iterable

from desktop.lib.models.baseprogress import CheckoutProgress, BaseProgress, RevertProgress
from desktop.lib.models.branch import AheadBehind
from desktop.lib.models.branches_state import BranchesState
from desktop.lib.models.changes_selection import ChangesSelection, ChangesWorkingDirectorySelection
from desktop.lib.models.changes_state import ChangesState
from desktop.lib.models.commit import Commit
from desktop.lib.models.commit_identity import CommitIdentity
from desktop.lib.models.commit_message import kDefaultCommitMessage
from desktop.lib.models.commit_selection import CommitSelection
from desktop.lib.models.compare_state import CompareState, DisplayHistory, InferredComparisonBranch
from desktop.lib.models.github_user import GitHubUser
from desktop.lib.models.rebase_state import RebaseState
from desktop.lib.models.remote import Remote
from desktop.lib.models.tip import UnknownRepository
from desktop.lib.models.working_directory_status import WorkingDirectoryStatus
from desktop.lib.stores.comparison_cache import ComparisonCache


@dataclass
class RepositoryState:
    commit_selection: CommitSelection
    changes_state: ChangesState
    compare_state: CompareState
    commit_author: Optional[CommitIdentity]
    branches_state: BranchesState
    rebase_state: RebaseState

    github_users: Mapping[str, GitHubUser]
    commit_lookup: Mapping[str, Commit]

    local_commit_shas: Iterable[str]
    remote: Optional[Remote]
    ahead_behind: Optional[AheadBehind]
    is_push_pull_fetch_in_progress: bool
    is_committing: bool
    last_fetched: Optional[datetime]

    checkout_progress: Optional[CheckoutProgress]

    push_pull_fetch_progress: Optional[BaseProgress]

    revert_progress: Optional[RevertProgress]

    @classmethod
    def create_initial_repository_state(cls) -> 'RepositoryState':
        return RepositoryState(commit_selection=CommitSelection(
            sha=None,
            file=None,
            changed_files=[],
            diff=None
        ),
            changes_state=ChangesState(
                working_directory=WorkingDirectoryStatus(),
                selection=ChangesWorkingDirectorySelection(),
                commit_message=kDefaultCommitMessage,
                coauthors=[],
                show_coauthor_by=False,
                conflict_state=None,
                stash_entry=None,
                current_branch_protected=False
            ),
            branches_state=BranchesState(
                tip=UnknownRepository(),
                default_branch=None,
                all_branches=[],
                recent_branches=[],
                open_pull_requests=[],
                current_pull_request=None,
                is_loading_pull_requests=False,
                rebased_branches=dict()
            ),
            compare_state=CompareState(
                is_diverging_branch_banner_visible=False,
                form_state=DisplayHistory(),
                tip=None,
                merge_status=None,
                show_branch_list=False,
                filter_text='',
                commit_shas=[],
                ahead_behind_cache=ComparisonCache(),
                all_branches=[],
                recent_branches=[],
                default_branch=None,
                inferred_comparison_branch=InferredComparisonBranch(
                    branch=None,
                    ahead_behind=None
                )
            ),
            rebase_state=RebaseState(
                step=None,
                progress=None,
                commits=None,
                user_has_resolved_conflicts=False
            ),
            commit_author= None,
            github_users={},
            commit_lookup={},
            local_commit_shas=[],
            ahead_behind=None,
            remote=None,
            is_push_pull_fetch_in_progress=False,
            is_committing=False,
            last_fetched=None,
            checkout_progress=None,
            push_pull_fetch_progress=None,
            revert_progress=None

        )
