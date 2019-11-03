from desktop.lib.git.errors import GitCmdStatusCode
from desktop.lib.git.interpret_trailers import get_trailer_separator_characters, parse_raw_unfolded_trailers
from desktop.lib.git.spawn import git
from desktop.lib.models.branch import BranchType, Branch
from desktop.lib.models.commit import Commit
from desktop.lib.models.commit_identity import CommitIdentity
from desktop.lib.models.repository import Repository

ForksReferencesPrefix = f'refs/remotes/github-desktop-'


async def get_branches(repository: Repository, *args):
    delimiter = chr(int('1F', 16))

    format = '%00'.join([
        '%(refname)',
        '%(refname:short)',
        '%(upstream:short)',
        '%(objectname)',  # SHA
        '%(objectname:short)',  # short SHA
        '%(author)',
        '%(committer)',
        '%(parent)',  # parent SHAs
        '%(symref)',
        '%(subject)',
        '%(body)',
        '%(trailers:unfold,only)',
        f'%{delimiter}'  # indicate end-of-line as %(body) may contain newlines
    ])

    prefixes = args
    if not prefixes:
        prefixes = ['refs/heads', 'refs/remotes']

    git_result = await git(
        ['for-each-ref', f'--format={format}', *prefixes],
        repository.path)

    if git_result.status_code == GitCmdStatusCode.NotAGitRepository:
        return []

    names = git_result.stdout
    lines = names.split(delimiter)
    lines = lines[:-1]
    if len(lines) == 0:
        return []

    trailer_separators = await get_trailer_separator_characters(repository)
    branches = []

    for idx, line in enumerate(lines):
        line = line[1:] if idx > 0 else line
        pieces = line.split('\0')

        ref = pieces[0]
        name = pieces[1]
        upstream = pieces[2]
        sha = pieces[3]
        short_sha = pieces[4]

        author_identity = pieces[5]
        author = CommitIdentity.parse_identity(author_identity)

        if not author:
            raise Exception(f"Couldn't parse author identity {author_identity}")

        committer_identity = pieces[6]
        committer = CommitIdentity.parse_identity(committer_identity)
        if not committer:
            raise Exception(f"Couldn't parse committer identity {committer_identity}")

        parent_shas = pieces[7].split(' ')
        symref = pieces[8]
        summary = pieces[9]
        body = pieces[10]
        trailers = parse_raw_unfolded_trailers(pieces[11], trailer_separators)

        tip = Commit(
            sha=sha,
            short_sha=short_sha,
            summary=summary,
            body=body,
            author=author,
            committer=committer,
            parent_shas=parent_shas,
            trailers=trailers
        )

        type = BranchType.Local if ref.startswith('refs/head') else BranchType.Remote

        if len(symref) > 0:
            continue

        if ref.startswith(ForksReferencesPrefix):
            # hide refs from our known remotes as these are considered plumbing
            # and can add noise to everywhere in the user interface where we
            # display branches as forks will likely contain duplicates of the same
            # ref names
            continue

        branches.append(Branch(
            name=name,
            upstream=upstream if upstream else None,
            tip=tip,
            type=type
        ))
    return branches
