from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import Tuple, Optional

from typing_extensions import Literal

from desktop.lib.git.status import WorkingDirectoryFileChange
from desktop.lib.models.preferences_tab import PreferencesTab
from .branch import Branch
from .repository import Repository


class PopupType(IntEnum):
    RenameBranch = 1
    DeleteBranch = auto()
    ConfirmDiscardChanges = auto()
    Preferences = auto()
    MergeBranch = auto()
    RepositorySettings = auto()
    AddRepository = auto()
    CreateRepository = auto()
    CloneRepository = auto()
    CreateBranch = auto()
    SignIn = auto()
    About = auto()
    InstallGit = auto()
    PublishRepository = auto()
    Acknowledgements = auto()
    UntrustedCertificate = auto()
    RemoveRepository = auto()
    TermsAndConditions = auto()
    PushBranchCommits = auto()
    CLIInstalled = auto()
    GenericGitAuthentication = auto()
    ExternalEditorFailed = auto()
    OpenShellFailed = auto()
    InitializeLFS = auto()
    LFSAttributeMismatch = auto()
    UpstreamAlreadyExists = auto()
    ReleaseNotes = auto()
    DeletePullRequest = auto()
    MergeConflicts = auto()
    AbortMerge = auto()
    OversizedFiles = auto()
    UsageReportingChanges = auto()
    CommitConflictsWarning = auto()
    PushNeedsPull = auto()
    RebaseFlow = auto()
    ConfirmForcePush = auto()
    StashAndSwitchBranch = auto()
    ConfirmOverwriteStash = auto()
    ConfirmDiscardStash = auto()
    CreateTutorialRepository = auto()


@dataclass(frozen=True)
class RenameBranchPopup:
    type: Literal[PopupType.RenameBranch] = field(init=False, default=PopupType.RenameBranch)
    repository: Repository
    branch: Branch


@dataclass(frozen=True)
class DeleteBranchPopup:
    type: Literal[PopupType.DeleteBranch] = field(init=False, default=PopupType.DeleteBranch)
    repository: Repository
    branch: Branch
    exists_on_remote: bool


@dataclass(frozen=True)
class ConfirmDiscardChangesPopup:
    type: Literal[PopupType.ConfirmDiscardChanges] = field(init=False, default=PopupType.ConfirmDiscardChanges)
    repository: Repository
    files: Tuple[WorkingDirectoryFileChange, ...]
    show_discard_changes_setting: Optional[bool]
    discarding_all_changes: Optional[bool]


@dataclass(frozen=True)
class PreferencesPopup:
    type: Literal[PopupType.Preferences] = field(init=False, default=PopupType.Preferences)
    initial_selected_tab: Optional[PreferencesTab]


@dataclass(frozen=True)
class RepositorySettingsPopup:
    type: Literal[PopupType.RepositorySettings] = field(init=False, default=PopupType.RepositorySettings)
    repository: Repository


@dataclass(frozen=True)
class AddRepositoryPopup:
    type: Literal[PopupType.AddRepository] = field(init=False, default=PopupType.AddRepository)
    path: Optional[str]


@dataclass(frozen=True)
class CreateRepositoryPopup:
    type: Literal[PopupType.CreateRepository] = field(init=False, default=PopupType.CreateRepository)
    path: Optional[str]


@dataclass(frozen=True)
class CloneRepositoryPopup:
    type: Literal[PopupType.CloneRepository] = field(init=False, default=PopupType.CloneRepository)
    initial_url: Optional[str]


@dataclass(frozen=True)
class CreateBranchPopup:
    type: Literal[PopupType.CreateBranch] = field(init=False, default=PopupType.CreateBranch)
    repository: Repository
    handle_protected_branch_warning: Optional[bool]
    initial_name: Optional[str]

@dataclass(frozen=True)
class SignInPopup:
    type: Literal[PopupType.SignIn] = field(init=False, default=PopupType.SignIn)


@dataclass(frozen=True)
class AboutPopup:


