import json
import logging
import platform
from dataclasses import dataclass
from enum import Enum
from typing import *
from urllib.parse import urljoin, quote

import aiohttp as http
from dataclasses_json import dataclass_json


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    HEAD = 'HEAD'


@dataclass_json
@dataclass
class ErrorData:
    message: str
    resource: str
    field: str


@dataclass_json
@dataclass
class APIErrorData:
    errors: Optional[List[ErrorData]] = None
    message: Optional[str] = None


@dataclass
class APIError(Exception):
    apiError: Optional[APIErrorData] = None

    def __init__(self, response: http.ClientResponse,
                 api_error: Optional[APIErrorData]):
        if api_error and api_error.message:
            message = api_error.message

            additional_messages = ', '.join([e.message for e in api_error.errors] if api_error.errors else [])

            if additional_messages:
                message = f'{message} ({additional_messages})'
        else:
            message = f'API error {response.url}:(${response.status})'

        super().__init__(message)
        self.apiError = api_error


T = TypeVar('T')


def load(cls, value: str):
    return cls.from_json(value)


async def deserialize_object(response: http.ClientResponse, cls) -> T:
    try:
        return await response.json(loads=cls.from_json)
    except Exception as e:
        content_length = response.headers.get('Content-Length') or '(missing)'
        request_id = response.headers.get('X-GitHub-Request-Id') or '(missing)'
        logging.warning(
            f"deserialize: invalid JSON found at '{response.url}' - status: {response.status}, length: {content_length}, requestId: {request_id}",
            e)

        raise e


async def deserialize_list(response: http.ClientResponse, cls) -> List[T]:
    def ignore_unknown(data: str):
        return [cls.from_dict(l) for l in json.loads(data)]

    try:
        return await response.json(loads=ignore_unknown)
    except Exception as e:
        content_length = response.headers.get('Content-Length') or '(missing)'
        request_id = response.headers.get('X-GitHub-Request-Id') or '(missing)'
        logging.warning(
            f"deserialize: invalid JSON found at '{response.url}' - status: {response.status}, length: {content_length}, requestId: {request_id}",
            e)

        raise e


def get_absolute_url(endpoint: str, path: str) -> str:
    relative_path = path[1:] if path[0] == '/' else path

    if relative_path.startswith('api/v3/'):
        relative_path = relative_path[7:]

    base = endpoint if endpoint.endswith('/') else f"{endpoint}/"
    return urljoin(base, relative_path)


# make an api request
async def request(
        session: http.ClientSession,
        endpoint: str,
        token: Optional[str],
        method: HTTPMethod,
        path: str,
        json_body: Optional[T] = None,
        custom_headers: Optional[Mapping[str, str]] = None) -> http.ClientResponse:
    url = get_absolute_url(endpoint, path)
    headers = {
        'Accept': 'application/vnd.github.v3+json, application/json',
        'Content-Type': 'application/json',
        'User-Agent': get_user_agent()
    }

    if token:
        headers['Authorization'] = f"token {token}"

    if custom_headers:
        headers = dict(headers, **custom_headers)

    return await session.request(method.value,
                                 url,
                                 headers=headers,
                                 json=json_body)


def get_user_agent():
    name = platform.system()
    return f'GitHubDesktop/({name})'


def url_with_query_string(url: str, **kwargs) -> str:
    qs = '&'.join(["{}={}".format(key, quote(value, safe='~()*!.\'')) for key, value in kwargs.items()])
    if not qs:
        return url

    if url.find('?') == -1:
        return f'{url}?{qs}'
    else:
        return f'{url}&{qs}'
