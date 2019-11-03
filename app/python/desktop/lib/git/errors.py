from enum import IntEnum
import re

from desktop.lib.fatal_error import assert_never


class GitCmdStatusCode(IntEnum):
    Success = 0
    SSHKeyAuditUnverified = 1
    SSHAuthenticationFailed = 2
    SSHPermissionDenied = 3
    HTTPSAuthenticationFailed = 4
    RemoteDisconnection = 5
    HostDown = 6
    RebaseConflicts = 7
    MergeConflicts = 8
    HTTTPSRepositoryNotFound = 9
    SSHRepositoryNotFound = 10
    PushNotFastForward = 11
    BranchDeletionFailed = 12
    DefaultBranchDeletionFailed = 13
    RevertConflicts = 14
    EmptyRebasePath = 15
    NoMatchingRemoteBranch = 16
    NoExistingRemoteBranch = 17
    NothingToCommit = 18
    NoSubmoduleMapping = 19
    SubmoduleRepositoryDoesNotExist = 20
    InvalidSubmoduleSHA = 21
    LocalPermissionDenied = 22
    InvalidMerge = 23
    InvalidRebase = 24
    NonFastForwardMergeIntoEmptyHead = 25
    PatchDoesNotApply = 26
    BranchAlreadyExists = 27
    BadRevision = 28
    NotAGitRepository = 29
    CannotMergeUnrelatedHistories = 30
    LFSAttributeDoesNotMatch = 31
    BranchRenameFailed = 32
    PathDoesNotExist = 33
    InvalidObjectName = 34
    OutsideRepository = 35
    LockFileAlreadyExists = 36
    NoMergeToAbort = 37
    LocalChangesOverwritten = 38
    UnresolvedConflicts = 39
    PushWithFileSizeExceedingLimit = 40
    HexBranchNameRejected = 41
    ForcePushRejected = 42
    InvalidRefLength = 43
    ProtectedBranchRequiresReview = 44
    ProtectedBranchForcePush = 45
    ProtectedBranchDeleteRejected = 46
    ProtectedBranchRequiredStatus = 47
    PushWithPrivateEmail = 48
    GitNotFoundErrorCode = 49
    RepositoryDoesNotExistErrorCode = 50


# A mapping from regexes to the git error they identify
GitErrorRegexes = {
    re.compile(
        r"ERROR: ([\s\S]+?)\n+\[EPOLICYKEYAGE\]\n+fatal: Could not read from remote repository."): GitCmdStatusCode.SSHKeyAuditUnverified,
    re.compile(r"fatal: Authentication failed for 'https://"): GitCmdStatusCode.HTTPSAuthenticationFailed,
    re.compile(r"fatal: Authentication failed"): GitCmdStatusCode.SSHAuthenticationFailed,
    re.compile(r"fatal: Could not read from remote repository."): GitCmdStatusCode.SSHPermissionDenied,
    re.compile(r"The requested URL returned error: 403"): GitCmdStatusCode.HTTPSAuthenticationFailed,
    re.compile(r"fatal: The remote end hung up unexpectedly"): GitCmdStatusCode.RemoteDisconnection,
    re.compile(r"fatal: unable to access '(.+)': Failed to connect to (.+):Host is down"): GitCmdStatusCode.HostDown,
    re.compile(
        r"Cloning into '(.+)'...\nfatal: unable to access '(.+)': Could not resolve host: (.+)"): GitCmdStatusCode.HostDown,
    re.compile(r"Failed to merge in the changes."): GitCmdStatusCode.RebaseConflicts,
    re.compile(
        r"(Merge conflict|Automatic merge failed; fix conflicts and then commit the result)"): GitCmdStatusCode.MergeConflicts,
    re.compile(r"fatal: repository '(.+)' not found"): GitCmdStatusCode.HTTTPSRepositoryNotFound,
    re.compile(r"ERROR: Repository not found"): GitCmdStatusCode.SSHRepositoryNotFound,
    re.compile(
        r"\((non-fast-forward|fetch first)\)\nerror: failed to push some refs to '.*'"): GitCmdStatusCode.PushNotFastForward,
    re.compile(r"error: unable to delete '(.+)': remote ref does not exist"): GitCmdStatusCode.BranchDeletionFailed,
    re.compile(
        r"Applying: .*\nNo changes - did you forget to use 'git add'\?\nIf there is nothing left to stage, chances are that something else\n.*"): GitCmdStatusCode.EmptyRebasePath,
    re.compile(
        r"There are no candidates for (rebasing|merging) among the refs that you just fetched.\nGenerally this means that you provided a wildcard refspec which had no\nmatches on the remote end"): GitCmdStatusCode.NoMatchingRemoteBranch,
    re.compile(
        r"Your configuration specifies to merge with the ref '(.+)'\nfrom the remote, but no such ref was fetched."): GitCmdStatusCode.NoExistingRemoteBranch,
    re.compile(r"nothing to commit"): GitCmdStatusCode.NothingToCommit,
    re.compile(r"No submodule mapping found in .gitmodules for path '(.+)'"): GitCmdStatusCode.NoSubmoduleMapping,
    re.compile(
        r"fatal: repository '(.+)' does not exist\nfatal: clone of '.*' into submodule path '(.+)' failed"): GitCmdStatusCode.SubmoduleRepositoryDoesNotExist,
    re.compile(
        r"Fetched in submodule path '(.+)', but it did not contain (.+). Direct fetching of that commit failed."): GitCmdStatusCode.InvalidSubmoduleSHA,
    re.compile(
        r"fatal: could not create work three dir '(.+)'.*: Permission denied"): GitCmdStatusCode.LocalPermissionDenied,
    re.compile(r"merge: (.+) - not something we can merge"): GitCmdStatusCode.InvalidMerge,
    re.compile(r"invalid upstream (.+)'"): GitCmdStatusCode.InvalidRebase,
    re.compile(
        r"fatal: Non-fast-forward commit does not make sense into an empty head"): GitCmdStatusCode.NonFastForwardMergeIntoEmptyHead,
    re.compile(
        r"error: (.+): (patch does not apply|already exists in working directory)"): GitCmdStatusCode.PatchDoesNotApply,
    re.compile(r"fatal: A branch named '(.+)' already exists."): GitCmdStatusCode.BranchAlreadyExists,
    re.compile(r"fatal: bad revision '(.*)' already exists."): GitCmdStatusCode.BadRevision,
    re.compile(
        r"fatal: [Nn]ot a git repository \(or any of the parent directories\): (.*)"): GitCmdStatusCode.NotAGitRepository,
    re.compile(r"fatal: refusing to merge unrelated histories"): GitCmdStatusCode.CannotMergeUnrelatedHistories,
    re.compile(r"The .+ attribute should be .+ but is .+"): GitCmdStatusCode.LFSAttributeDoesNotMatch,
    re.compile(r"fatal: Branch rename failed"): GitCmdStatusCode.BranchRenameFailed,
    re.compile(r"fatal: Path '(.+)' does not exitst .+"): GitCmdStatusCode.PathDoesNotExist,
    re.compile(r"fatal: Invalid object name '(.+)'."): GitCmdStatusCode.InvalidObjectName,
    re.compile(r"fatal: .+: '(.+)' is outside repository"): GitCmdStatusCode.OutsideRepository,
    re.compile(
        r"Another git process seems to be running in this repository, e.g."): GitCmdStatusCode.LockFileAlreadyExists,
    re.compile(r"fatal: There is no merge to abort"): GitCmdStatusCode.NoMergeToAbort,
    re.compile(
        r"error: (?:Your local changes to the following|The following untracked working tree) files would be overwritten by checkout:"): GitCmdStatusCode.LocalChangesOverwritten,
    re.compile(
        r"You must edit all merge conflicts and then\nmark them as resolved using git add"): GitCmdStatusCode.UnresolvedConflicts,
    # GitHub-specific errors
    re.compile(r"error: GH001: "): GitCmdStatusCode.PushWithFileSizeExceedingLimit,
    re.compile(r"error: GH002: "): GitCmdStatusCode.HexBranchNameRejected,
    re.compile(r"error: GH003: Sorry, force-pushing to (.+) is not allowed."): GitCmdStatusCode.ForcePushRejected,
    re.compile(r"error: GH005: Sorry, refs longer than (.+) bytes are not allowed"): GitCmdStatusCode.InvalidRefLength,
    re.compile(
        r"error: GH006: Protected branch update failed for (.+)\nremote: error: At least one approved review is required"): GitCmdStatusCode.ProtectedBranchRequiresReview,
    re.compile(
        r"error: GH006: Protected branch update failed for (.+)\nremote: error: Cannot force-push to a protected branch"): GitCmdStatusCode.ProtectedBranchForcePush,
    re.compile(
        r"error: GH006: Protected branch update failed for (.+)\nremote: error: Cannot delete a protected branch"): GitCmdStatusCode.ProtectedBranchDeleteRejected,
    re.compile(
        r'error: GH006: Protected branch update failed for (.+).\nremote: error: Required status check "(.+)" is expected'): GitCmdStatusCode.ProtectedBranchRequiredStatus,
    re.compile(r"error: GH007: Your push would publish a private email address."): GitCmdStatusCode.PushWithPrivateEmail
}


def get_description_for_error(error: GitCmdStatusCode) -> str:
    if error == GitCmdStatusCode.SSHKeyAuditUnverified:
        return 'The SSH key is unverified.'
    if error == GitCmdStatusCode.SSHAuthenticationFailed or error == GitCmdStatusCode.SSHPermissionDenied or error == GitCmdStatusCode.HTTPSAuthenticationFailed:
        menu_hint = "File > Options"
        return "Authentication failed. Some common reasons include:" + \
               f"- You are not logged in to your account: see {menu_hint}" + \
               "- You may need to log out and log back in to refresh your token." + \
               "- You do not have permission to access this repository." + \
               "- The repository is archived on GitHub. Check the repository settings to confirm you are still permitted to push commits." + \
               "- If you use SSH authentication, check that your key is added to the ssh-agent and associated with your account."
    if error == GitCmdStatusCode.RemoteDisconnection:
        return 'The remote disconnected. Check your Internet connection and try again.'
    if error == GitCmdStatusCode.HostDown:
        return 'The host is down. Check your Internet connection and try again.'
    if error == GitCmdStatusCode.RebaseConflicts:
        return 'We found some conflicts while trying to rebase. Please resolve the conflicts before continuing.'
    if error == GitCmdStatusCode.MergeConflicts:
        return 'We found some conflicts while trying to merge. Please resolve the conflicts and commit the changes.'
    if error == GitCmdStatusCode.HTTPSRepositoryNotFound or error == GitCmdStatusCode.SSHRepositoryNotFound:
        return 'The repository does not seem to exist anymore. You may not have access, or it may have been deleted or renamed.'
    if error == GitCmdStatusCode.PushNotFastForward:
        return 'The repository has been updated since you last pulled. Try pulling before pushing.'
    if error == GitCmdStatusCode.BranchDeletionFailed:
        return 'Could not delete the branch. It was probably already deleted.'
    if error == GitCmdStatusCode.DefaultBranchDeletionFailed:
        return "The branch is the repository's default branch and cannot be deleted."
    if error == GitCmdStatusCode.RevertConflicts:
        return 'To finish reverting, please merge and commit the changes.'
    if error == GitCmdStatusCode.EmptyRebasePatch:
        return 'There aren’t any changes left to apply.'
    if error == GitCmdStatusCode.NoMatchingRemoteBranch:
        return 'There aren’t any remote branches that match the current branch.'
    if error == GitCmdStatusCode.NothingToCommit:
        return 'There are no changes to commit.'
    if error == GitCmdStatusCode.NoSubmoduleMapping:
        return 'A submodule was removed from .gitmodules, but the folder still exists in the repository. Delete the folder, commit the change, then try again.'
    if error == GitCmdStatusCode.SubmoduleRepositoryDoesNotExist:
        return 'A submodule points to a location which does not exist.'
    if error == GitCmdStatusCode.InvalidSubmoduleSHA:
        return 'A submodule points to a commit which does not exist.'
    if error == GitCmdStatusCode.LocalPermissionDenied:
        return 'Permission denied.'
    if error == GitCmdStatusCode.InvalidMerge:
        return 'This is not something we can merge.'
    if error == GitCmdStatusCode.InvalidRebase:
        return 'This is not something we can rebase.'
    if error == GitCmdStatusCode.NonFastForwardMergeIntoEmptyHead:
        return 'The merge you attempted is not a fast-forward, so it cannot be performed on an empty branch.'
    if error == GitCmdStatusCode.PatchDoesNotApply:
        return 'The requested changes conflict with one or more files in the repository.'
    if error == GitCmdStatusCode.BranchAlreadyExists:
        return 'A branch with that name already exists.'
    if error == GitCmdStatusCode.BadRevision:
        return 'Bad revision.'
    if error == GitCmdStatusCode.NotAGitRepository:
        return 'This is not a git repository.'
    if error == GitCmdStatusCode.ProtectedBranchForcePush:
        return 'This branch is protected from force-push operations.'
    if error == GitCmdStatusCode.ProtectedBranchRequiresReview:
        return 'This branch is protected and any changes requires an approved review. Open a pull request with changes targeting this branch instead.'
    if error == GitCmdStatusCode.PushWithFileSizeExceedingLimit:
        return "The push operation includes a file which exceeds GitHub's file size restriction of 100MB. Please remove the file from history and try again."
    if error == GitCmdStatusCode.HexBranchNameRejected:
        return 'The branch name cannot be a 40-character string of hexadecimal characters, as this is the format that Git uses for representing objects.'
    if error == GitCmdStatusCode.ForcePushRejected:
        return 'The force push has been rejected for the current branch.'
    if error == GitCmdStatusCode.InvalidRefLength:
        return 'A ref cannot be longer than 255 characters.'
    if error == GitCmdStatusCode.CannotMergeUnrelatedHistories:
        return 'Unable to merge unrelated histories in this repository.'
    if error == GitCmdStatusCode.PushWithPrivateEmail:
        return 'Cannot push these commits as they contain an email address marked as private on GitHub.'
    if error == GitCmdStatusCode.LFSAttributeDoesNotMatch:
        return 'Git LFS attribute found in global Git configuration does not match expected value.'
    if error == GitCmdStatusCode.ProtectedBranchDeleteRejected:
        return 'This branch cannot be deleted from the remote repository because it is marked as protected.'
    if error == GitCmdStatusCode.ProtectedBranchRequiredStatus:
        return 'The push was rejected by the remote server because a required status check has not been satisfied.'
    if error == GitCmdStatusCode.BranchRenameFailed:
        return 'The branch could not be renamed.'
    if error == GitCmdStatusCode.PathDoesNotExist:
        return 'The path does not exist on disk.'
    if error == GitCmdStatusCode.InvalidObjectName:
        return 'The object was not found in the Git repository.'
    if error == GitCmdStatusCode.OutsideRepository:
        return 'This path is not a valid path inside the repository.'
    if error == GitCmdStatusCode.LockFileAlreadyExists:
        return 'A lock file already exists in the repository, which blocks this operation from completing.'
    if error == GitCmdStatusCode.NoMergeToAbort:
        return 'There is no merge in progress, so there is nothing to abort.'
    if error == GitCmdStatusCode.NoExistingRemoteBranch:
        return 'The remote branch does not exist.'
    if error == GitCmdStatusCode.LocalChangesOverwritten:
        return 'Unable to switch branches as there are working directory changes which would be overwritten. Please commit or stash your changes.'
    if error == GitCmdStatusCode.UnresolvedConflicts:
        return 'There are unresolved conflicts in the working directory.'

    return assert_never(error, "Unknown error: ${error}")
