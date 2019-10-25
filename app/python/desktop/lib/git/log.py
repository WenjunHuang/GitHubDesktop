from typing import Iterable

from desktop.lib.git.interpret_trailers import get_trailer_separator_characters, parse_raw_unfolded_trailers
from desktop.lib.git.spawn import git
from desktop.lib.models.commit import Commit
from desktop.lib.models.commit_identity import CommitIdentity
from desktop.lib.models.repository import Repository


async def get_commits(repository: Repository,
                      revision_range: str,
                      limit: int,
                      additional_args: Iterable[str] = []) -> Iterable[Commit]:
    delimiter = '1F'
    delimiter_string = chr(int(delimiter, 16))
    pretty_format = f"%x{delimiter}".join([
        '%H',
        '%h',
        '%s',
        '%b',
        '%an <%ae> %ad',
        '%cn <%ce> %cd',
        '%P',
        '%(trailers:unfold,only)'
    ])

    stdout, stderr, return_code = await git([
        'log',
        revision_range,
        '--date=raw',
        f'--max-count={limit}',
        f'--pretty={pretty_format}',
        '-z',
        '--no-show-signature',
        '--no-color',
        *additional_args,
        '--'
    ], repository.path)

    if return_code == 128:
        return []

    if stderr:
        err = stderr.decode('utf-8')
        print(err)

    out = stdout.decode('utf-8')
    lines = out.split('\0')
    lines = lines[:-1]
    if len(lines) == 0:
        return []

    trailer_separators = await get_trailer_separator_characters(repository)
    commits = [line_to_commit(line, delimiter_string, trailer_separators) for line in lines]

    return commits


def line_to_commit(line: str, delimiter_str: str, trailer_separators: str) -> Commit:
    pieces = line.split(delimiter_str)
    sha = pieces[0]
    short_sha = pieces[1]
    summary = pieces[2]
    body = pieces[3]
    author_identity = pieces[4]
    committer_identity = pieces[5]
    sha_list = pieces[6]

    parent_shas = [] if not sha_list else sha_list.split(' ')
    trailers = parse_raw_unfolded_trailers(pieces[7], trailer_separators)

    author = CommitIdentity.parse_identity(author_identity)
    if not author:
        raise Exception(f"Couldn't parse author identity {author_identity}")

    committer = CommitIdentity.parse_identity(committer_identity)
    if not committer:
        raise Exception(f"Couldn't parse commiter identity {committer_identity}")

    return Commit(
        sha=sha,
        short_sha=short_sha,
        summary=summary,
        body=body,
        author=author,
        committer=committer,
        parent_shas=parent_shas,
        trailers=trailers
    )
