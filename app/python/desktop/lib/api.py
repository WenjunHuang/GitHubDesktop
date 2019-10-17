import base64
import os
import re
import socket
from abc import ABC
from dataclasses import field
from datetime import datetime
from enum import IntEnum
from urllib.parse import urlsplit, urlunsplit, unquote
from uuid import uuid4

from dataclasses_json import config

from desktop.lib.common import with_logger, get_machine_username
from desktop.lib.http import *
from desktop.lib.two_factor_auth import AuthenticationMode


class MaxResultsError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


kScopes = ['repo', 'user']

# dev
kClientId = '3a723b10ac5575cc5bb9'
kClientSecret = '22c34d87789a365981ed921352a7b9a8c3f69d54'
kNoteURL = 'https://desktop.github.com/'


class GitHubAccountType(Enum):
    User = 'User'
    Organization = 'Organization'

    @classmethod
    def from_str(cls, value: str) -> 'GitHubAccountType':
        return GitHubAccountType(value)


class IssueState(Enum):
    Open = 'open'
    Closed = 'closed'
    All = 'all'

    @classmethod
    def from_str(cls, value: str) -> 'IssueState':
        return IssueState(value)


@dataclass_json
@dataclass
class APIIssueData:
    number: int
    title: str
    state: IssueState = field(
        metadata=config(
            encoder=IssueState,
            decoder=IssueState.from_str
        )
    )
    updated_at: str
    pullRequest: Optional[bool] = None
    # pull_request: bool


@dataclass_json
@dataclass
class APIFullIdentityData:
    id: int
    url: str
    login: str
    avatar_url: str
    type: GitHubAccountType = field(
        metadata=config(
            encoder=GitHubAccountType,
            decoder=GitHubAccountType.from_str
        )
    )
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass_json
@dataclass
class APIIdentityData:
    id: int
    url: str
    login: str
    avatar_url: str
    type: GitHubAccountType = field(
        metadata=config(
            encoder=GitHubAccountType,
            decoder=GitHubAccountType.from_str
        )
    )


@dataclass_json
@dataclass
class APIRepositoryData:
    clone_url: str
    ssh_url: str
    html_url: str
    name: str
    owner: APIIdentityData
    private: bool
    fork: bool
    default_branch: str
    pushed_at: str
    parent: Optional['APIRepositoryData'] = None


class EmailVisibility(Enum):
    Public = 'public'
    Private = 'private'

    @classmethod
    def from_str(cls, value: str):
        if not str:
            return None
        return EmailVisibility(value)


@dataclass_json
@dataclass
class APIEmailData:
    email: str
    verified: bool
    primary: bool
    visibility: Optional[EmailVisibility] = field(
        metadata=config(
            encoder=EmailVisibility,
            decoder=EmailVisibility.from_str
        )
    )


@dataclass_json
@dataclass
class APISearchForUsersResults:
    items: List[APIIdentityData]


@dataclass_json
@dataclass
class APICommitData:
    sha: str
    author: Optional[APIIdentityData] = None


@dataclass_json
@dataclass
class APIOrganizationData:
    id: int
    url: str
    login: str
    avatar_url: str


class PullRequestState(Enum):
    Open = 'open'
    Closed = 'closed'

    @classmethod
    def from_str(cls, value: str) -> 'PullRequestState':
        return PullRequestState(value)


@dataclass_json
@dataclass
class APIPullRequestRefData:
    ref: str
    sha: str


@dataclass_json
@dataclass
class APIPullRequestData:
    number: int
    title: str
    created_at: str
    updated_at: str
    user: APIIdentityData
    base: APIPullRequestRefData
    head: APIPullRequestRefData
    state: PullRequestState = field(
        metadata=config(
            encoder=PullRequestState,
            decoder=PullRequestState.from_str
        )
    )


class APIRefState(Enum):
    Failure = 'failure'
    Pending = 'pending'
    Success = 'success'

    @classmethod
    def from_str(cls, value: str) -> 'APIRefState':
        return APIRefState(value)


@dataclass_json
@dataclass
class APIRefStatusItemData:
    state: APIRefState = field(
        metadata=config(
            encoder=APIRefState,
            decoder=APIRefState.from_str
        )
    )
    target_url: str
    description: str
    context: str
    id: int


@dataclass_json
@dataclass
class APIRefStatusData:
    state: APIRefState = field(
        metadata=config(
            encoder=APIRefState,
            decoder=APIRefState.from_str
        )
    )
    total_count: int
    statuses: List[APIRefStatusItemData]


@dataclass_json
@dataclass
class APIBranchData:
    name: str
    protected: bool


@dataclass_json
@dataclass
class APIAccessTokenData:
    access_token: str
    scope: str
    token_type: str


@dataclass_json
@dataclass
class APIAuthorizationData:
    token: str


class IFetchAllOptions(ABC):
    def per_page(self) -> Optional[int]:
        pass

    def should_continue(self, result) -> bool:
        pass

    def next_page_path(self, response: aiohttp.ClientResponse) -> Optional[str]:
        pass

    def suppress_errors(self) -> bool:
        pass


def get_next_pagepath_from_link(response: aiohttp.ClientResponse) -> Optional[str]:
    '''Parses the link header from GitHub and returns the next path if one
        is present.
        If no link rel next header is found this method returns null.
    '''
    link_header = response.headers.get('Link')
    if not link_header:
        return None

    regex = re.compile('<([^>]+)>; rel="([^"]+)"')
    for part in link_header.split(','):
        match = regex.match(part.strip())
        if match and match[2] == 'next':
            t = urlsplit(match[1])
            next_url = urlunsplit(('', '', t.path, t.query, t.fragment))
            return next_url

    return None


def to_github_iso_datestring(time: datetime) -> str:
    return time.isoformat(timespec='seconds')


@with_logger
class API:
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.token = token
        self.session = get_session()

    async def fetch_repository(self, owner: str, name: str) -> Union[APIRepositoryData, None]:
        try:
            response = await self.__request(HTTPMethod.GET,
                                            f'repos/{owner}/{name}')
            if response.status == 404:
                logging.warning(f'fetch_repository: "{owner}/{name}" return a 404')
                return None
            else:
                return await parse_response(response, APIRepositoryData)
        except Exception as e:
            logging.warning(f'fetch_repository: an error occured for "{owner}/{name}', e)
            return None

    async def fetch_repositories(self) -> Union[List[APIRepositoryData], None]:
        try:
            return await self.__fetch_all("user/repos",
                                          APIRepositoryData)
        except Exception as e:
            logging.warning(f"fetch_repositories: {e}")
            raise e

    async def fetch_account(self) -> APIFullIdentityData:
        try:
            response = await self.__request(HTTPMethod.GET, 'user')
            return await parse_response(response, APIFullIdentityData)
        except Exception as e:
            logging.warning(f"fetch_account: failed with endpoint {self.endpoint}", e)
            raise e

    async def fetch_emails(self) -> List[APIEmailData]:
        try:
            response = await self.__request(HTTPMethod.GET, 'user/emails')
            return await parse_response(response, APIEmailData, is_list=True)
        except Exception as e:
            logging.warning(f"fetch_emails: failed with endpoint {self.endpoint}", e)
            return []

    async def fetch_commit(self, owner: str, name: str, sha: str) -> Optional[APICommitData]:
        try:
            path = f"repos/{owner}/{name}/commits/{sha}"
            response = await self.__request(HTTPMethod.GET, path)
            if response.status == 404:
                logging.warning(f"fetch_commit: '{path}' returned a 404")
                return None
            return await parse_response(response, APICommitData)
        except Exception as e:
            logging.warning(f"fetch_commit: returned an error '{owner}/{name}@{sha}'", e)
            return None

    async def search_for_user_with_email(self, email: str) -> Optional[APIIdentityData]:
        if not email:
            return None
        try:
            url = url_with_query_string('search/users', q=f"{email} in:email type:user")
            response = await self.__request(HTTPMethod.GET, url)
            result = await parse_response(response, APISearchForUsersResults)
            items = result.items
            if len(items) > 0:
                return items[0]
            else:
                return None
        except Exception as e:
            logging.warning(f"search_for_user_with_email: not found '{email}'", e)
            return None

    async def fetch_orgs(self) -> List[APIOrganizationData]:
        try:
            return await self.__fetch_all('user/orgs', APIOrganizationData)
        except Exception as e:
            logging.warning(f"fetch_orgs: failed with endpoint {self.endpoint}", e)
            return []

    async def create_repository(self, org: Optional[APIOrganizationData],
                                name: str,
                                description: str,
                                private: bool) -> APIRepositoryData:
        try:
            api_path = f"orgs/{org.login}/repos" if org else 'user/repos'
            response = await self.__request(HTTPMethod.POST,
                                            api_path, {
                                                'name': name,
                                                'description': description,
                                                'private': private
                                            })
            return await parse_response(response, APIRepositoryData)
        except APIError as e:
            if org:
                raise Exception(
                    f"Unable to create repository for organization {org.login}. Verify that it exists, that it's a paid organization, and that you have permission to create a repository there.")
            raise e
        except Exception as e:
            logging.warning(f"create_repository: failed with endpoint {self.endpoint}", e)
            raise Exception(
                "Unable to publish repository.Please check if you have an internet connection and try again. ")

    async def fetch_issues(self, owner: str, name: str, state: IssueState, since: Optional[datetime] = None) -> \
            Iterable[
                APIIssueData]:
        params = {'state': state.value}
        if since:
            params['since'] = to_github_iso_datestring(since)

        url = url_with_query_string(f"repos/{owner}/{name}/issues", **params)
        try:
            issues = await self.__fetch_all(url, APIIssueData)
            return list(filter(lambda i: not i.pullRequest, issues))
        except Exception as e:
            logging.warning(f"fetch_issues: failed for repository {owner}/{name}", e)
            raise e

    async def fetch_all_open_pull_requests(self, owner: str, name: str) -> List[APIPullRequestData]:
        url = url_with_query_string(f"repos/{owner}/{name}/pulls", state='open')
        try:
            return await self.__fetch_all(url, APIPullRequestData)
        except Exception as e:
            logging.warning(f"failed fetching open PRs for repository {owner}/{name}", e)
            raise e

    async def fetch_updated_pull_requests(self, owner: str, name: str, since: datetime, max_results: int = 320):
        url = url_with_query_string(f"repos/{owner}/{name}/pulls", state='all', sort='updated', direction='desc')
        try:
            prs = await self.__fetch_all(url, APIPullRequestData, FetchUpdatedPullRequestOpt(since, max_results))
            return list(filter(lambda i: datetime.fromisoformat(i.updated_at) >= since, prs))
        except Exception as e:
            logging.warning(f"failed fetching updated PRs for repository {owner}/{name}", e)
            raise e

    async def fetch_combined_ref_status(self, owner: str, name: str, ref: str) -> APIRefStatusData:
        path = f"repos/{owner}/{name}/commits/{ref}/status"
        response = await self.__request(HTTPMethod.GET, path)
        return await parse_response(response, APIRefStatusData)

    async def fetch_protected_branches(self, owner: str, name: str) -> List[APIBranchData]:
        path = f"repos/{owner}/{name}/branches?protected=true"
        try:
            response = await self.__request(HTTPMethod.GET, path)
            return await parse_response(response, APIBranchData, is_list=True)
        except Exception as e:
            logging.info("fetch_protected_branches unable to list protected brances", e)
            return []

    async def get_fetch_poll_interval(self, owner: str, name: str) -> Optional[int]:
        path = f"repos/{owner}/{name}/git"
        try:
            response = await self.__request(HTTPMethod.HEAD, path)
            interval = response.headers.get('x-poll-interval')
            if interval:
                parsed = int(interval, 10)
                return parsed
            else:
                return None
        except Exception as e:
            self._logger.warning(f"failed for {owner}/{name}", e)
            return None

    async def fetch_user(self, login: str) -> Optional[APIFullIdentityData]:
        path = f"users/{quote(login)}"
        try:
            response = await self.__request(HTTPMethod.GET, path)
            if response.status == 404:
                return None
            return await parse_response(response, APIFullIdentityData)
        except Exception as e:
            self._logger.warning(f"fetch_user: failed with endpoint {self.endpoint}", e)
            raise

    async def __fetch_all(self,
                          path: str,
                          cls,
                          options: Optional[IFetchAllOptions] = None) -> List:
        buf = []
        per_page = 100 if not options or not options.per_page() else options.per_page()
        next_path = url_with_query_string(path, per_page=str(per_page))

        while True:
            response = await self.__request(HTTPMethod.GET, next_path)
            if response.status != 200 and (options and options.suppress_errors()):
                logging.warning(f"fetch_all: '{path}' returned a {response.status}")
                return buf

            items = await parse_response(response, cls, is_list=True)
            buf.extend(items)

            next_path = None if not options else options.next_page_path(response)
            next_path = get_next_pagepath_from_link(response) if not next_path else next_path

            if not next_path or (options and not options.should_continue(buf)):
                break

        return buf

    async def __request(self,
                        method: HTTPMethod,
                        path: str,
                        body: Optional[Any] = None,
                        custom_headers: Optional[Mapping[str, str]] = None):
        return await request(self.session,
                             self.endpoint,
                             self.token,
                             method,
                             path,
                             body,
                             custom_headers)


class FetchUpdatedPullRequestOpt(IFetchAllOptions):

    def __init__(self, since: datetime, max_result: int):
        super().__init__()
        self.max_result = max_result
        self.since = since

    def per_page(self) -> Optional[int]:
        return 10

    def next_page_path(self, response: aiohttp.ClientResponse) -> Optional[str]:
        next_path = get_next_pagepath_from_link(response)
        if not next_path:
            return None

        splitted_url = urlsplit(next_path)
        query_list = [sub.partition('=') for sub in splitted_url.query.split('&')]
        query_dict = {left: unquote(right) for (left, _, right) in query_list}

        page_size = int(query_dict.get('per_page'), 10) if 'per_page' in query_dict else None
        page_number = int(query_dict.get('page'), 10) if 'page' in query_dict else None

        if not page_size or not page_number:
            return next_path

        current_page = page_number - 1
        received = current_page * page_size
        next_page_size = min(100, page_size * 2)

        if page_size != next_page_size and received % next_page_size == 0:
            query = {'per_page': next_page_size, 'page': f"{received // next_page_size + 1}"}
            return url_with_query_string(
                urlunsplit((splitted_url.scheme, splitted_url.netloc, splitted_url.path, '', '')),
                **query)
        else:
            return next_path

    def should_continue(self, results) -> bool:
        if len(results) >= self.max_result:
            raise MaxResultsError('got max pull requests, aborting')

        last = results[-1]
        return datetime.fromisoformat(last.updated_at) > self.since

    def suppress_errors(self) -> bool:
        return False


async def parse_response(response: aiohttp.ClientResponse, cls, is_list: bool = False):
    if response.status == 200 or response.status == 201:
        if not is_list:
            return await deserialize_object(response, cls)
        else:
            return await deserialize_list(response, cls)
    else:
        try:
            api_error = await deserialize_object(response, APIErrorData)
        except Exception as e:
            raise APIError(response, None)

        raise APIError(response, api_error)


# Get github.com's API endpoint.
def get_dotcom_api_endpoint() -> str:
    env_endpoint = os.environ[
        'DESKTOP_GITHUB_DOTCOM_API_ENDPOINT'] if 'DESKTOP_GITHUB_DOTCOM_API_ENDPOINT' in os.environ else None
    if env_endpoint:
        return env_endpoint
    return 'https://api.github.com'


class AuthorizationResponseKind(IntEnum):
    Authorized = 0
    Failed = 1
    TwoFactorAuthenticationRequired = 2
    UserRequiresVerification = 3
    PersonalAccessTokenBlocked = 4
    Error = 5
    EnterpriseTooOld = 6


@dataclass
class AuthorizationResponse:
    kind: AuthorizationResponseKind
    token: Optional[str] = None
    response: Optional[aiohttp.ClientResponse] = None
    type: Optional[AuthenticationMode] = None


# create an authorization with given login,password, and one-time password.
async def create_authorization(endpoint: str, login: str, password: str,
                               onetime_password: Optional[str] = None) -> AuthorizationResponse:
    creds = str(base64.encodebytes(f"{login}:{password}".encode('utf-8')), 'utf-8').strip()
    authorization = f"Basic {creds}"
    opt_header = {'X-GitHub-OTP': onetime_password} if onetime_password else {}
    note = get_note()

    response = await request(get_session(),
                             endpoint,
                             None,
                             HTTPMethod.POST,
                             'authorizations',
                             {
                                 'scopes': kScopes,
                                 'client_id': kClientId,
                                 'client_secret': kClientSecret,
                                 'note': note,
                                 'note_url': kNoteURL,
                                 'fingerprint': str(uuid4())
                             },
                             {
                                 'Authorization': authorization,
                                 **opt_header
                             })
    try:
        result = await parse_response(response, APIAuthorizationData)
        token = result.token
        if isinstance(token, str) and token:
            return AuthorizationResponse(kind=AuthorizationResponseKind.Authorized, token=token)
    except Exception as e:
        if response.status == 401:
            otp_response = response.headers.get('x-github-otp')
            if otp_response:
                pieces = otp_response.split(';')
                if len(pieces) == 2:
                    type = pieces[1].strip()
                    if type == 'app':
                        return AuthorizationResponse(kind=AuthorizationResponseKind.TwoFactorAuthenticationRequired,
                                                     type=AuthenticationMode.App)
                    elif type == 'sms':
                        return AuthorizationResponse(kind=AuthorizationResponseKind.TwoFactorAuthenticationRequired,
                                                     type=AuthenticationMode.Sms)
                    else:
                        return AuthorizationResponse(kind=AuthorizationResponseKind.Failed,
                                                     response=response)
            return AuthorizationResponse(kind=AuthorizationResponseKind.Failed,
                                         response=response)

        api_error = isinstance(e, APIError) and e.apiError
        if api_error:
            if response.status == 403 and api_error.message == 'This API can only be accessed with username and password Basic Auth':
                # Authorization API does not support providing personal access tokens
                return AuthorizationResponse(kind=AuthorizationResponseKind.PersonalAccessTokenBlocked)
            elif response.status == 422:
                if api_error.errors:
                    for error in api_error.errors:
                        is_expected_resource = error.message.lower() == 'oauthaccess'
                        is_expected_field = error.field.lower() == 'user'

                        if is_expected_resource and is_expected_field:
                            return AuthorizationResponse(kind=AuthorizationResponseKind.UserRequiresVerification)
                elif api_error.message == 'Invalid OAuth application client_id or secret.':
                    return AuthorizationResponse(kind=AuthorizationResponseKind.EnterpriseTooOld)

    return AuthorizationResponse(kind=AuthorizationResponseKind.Error, response=response)


# the not used for created authorizations.
def get_note() -> str:
    local_username = 'unknown'
    try:
        local_username = get_machine_username()
    except Exception as e:
        logging.error(f"get_note: unable to resolve machine username, using '{local_username}' as a fallback", e)

    return f"GitHub Desktop on {local_username}@{socket.gethostname()}"
