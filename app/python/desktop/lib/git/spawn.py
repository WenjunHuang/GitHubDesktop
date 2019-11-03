import asyncio
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Container, Set

from desktop.lib.git.errors import GitCmdStatusCode, GitErrorRegexes, get_description_for_error


class GitError(Exception):
    result: GitResult
    args: List[str]

    def __init__(self, result: GitResult, args: List[str]):
        super().__init__(get_result_message(result))
        self.name = 'GitError'
        self.result = result
        self.args = args


@dataclass
class GitExecutionOptions:
    stdin: Optional[str] = None
    success_return_codes: Set[int] = field(default={0})


@dataclass
class GitResult:
    status_code: GitCmdStatusCode
    return_code: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    git_error_description: Optional[str] = None

    def success(self):
        return self.status_code == GitCmdStatusCode.Success


async def git(args: List[str],
              path: str,
              opts: Optional[GitExecutionOptions] = None) -> GitResult:
    try:
        proc = await asyncio.create_subprocess_exec('git', *args,
                                                    stdin=asyncio.subprocess.PIPE,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE,
                                                    cwd=path)
        if opts and opts.stdin:
            proc.stdin.write(opts.stdin.encode('utf-8'))
            await proc.stdin.drain()

        stdout, stderr = await proc.communicate()

    except FileNotFoundError as e:
        result = GitResult(status_code=GitCmdStatusCode.GitNotFoundErrorCode)
        raise GitError(result, args)
    else:
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        returncode = proc.returncode

        status_code = None
        git_error_description = None
        acceptable_exit_code = True if opts and returncode in opts.success_return_codes else False

        if not acceptable_exit_code:
            status_code = parse_error(stderr)
            if not status_code:
                status_code = parse_error(stdout)

            git_error_description = get_description_for_error(status_code) if status_code else None
        else:
            status_code = GitCmdStatusCode.Success

        git_result = GitResult(status_code=status_code,
                               stdout=stdout,
                               stderr=stderr,
                               return_code=returncode,
                               git_error_description=git_error_description)
        if acceptable_exit_code:
            return git_result
        else:
            raise GitError(git_result, args)


def parse_error(stderr: str) -> Optional[GitCmdStatusCode]:
    for regex, error in GitErrorRegexes.items():
        if regex.match(stderr):
            return error
    return None


def get_result_message(result: GitResult):
    description = result.git_error_description
    if description:
        return description

    if result.stderr:
        return result.stderr
    elif result.stdout:
        return result.stdout
    else:
        return 'Unknown error'
