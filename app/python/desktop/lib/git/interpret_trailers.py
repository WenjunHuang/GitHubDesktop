from dataclasses import dataclass
from typing import Optional, List

from desktop.lib.git.config import get_config_value
from desktop.lib.git.spawn import git
from desktop.lib.models.repository import Repository


@dataclass
class Trailer:
    token: str
    value: str

    def is_coauthors(self):
        return self.token.lower() == 'co-authored-by'


# Parse a string containing only unfolded trailers produced by
# git-interpret-trailers --only-input --only-trailers --unfold or
# a derivative such as git log --format="%(trailers:only,unfold)
def parse_raw_unfolded_trailers(trailers: str,
                                separators: str):
    lines = trailers.split('\n')
    parsed_trailers = []
    for line in lines:
        trailer = parse_single_unfolded_trailer(line, separators)
        if trailer:
            parsed_trailers.append(trailer)
    return parsed_trailers


def parse_single_unfolded_trailer(line: str,
                                  separators: str) -> Optional[Trailer]:
    for separator in separators:
        idx = line.find(separator)
        if idx > 0:
            return Trailer(token=line[0:idx].strip(),
                           value=line[idx].strip())
    return None


async def get_trailer_separator_characters(repository: Repository):
    return await get_config_value(repository, 'trailer.separators') or ':'


async def parse_trailers(repository: Repository,
                         commit_message: str) -> List[Trailer]:
    opts = ['interpret-trailers', '--parse']
    stdout, stderr, returncode = await git(opts, repository.path, commit_message)

    trailers = stdout.decode('utf-8')
    if not trailers:
        return []

    separators = await get_trailer_separator_characters(repository)
    return parse_raw_unfolded_trailers(trailers, separators)
