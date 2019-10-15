from functools import singledispatch

from collections import abc
from typing import *
import json


@singledispatch
def json_generator(obj) -> str:
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        raise Exception('obj class is not decorated by @dataclass_json')


@json_generator.register(str)
def _(value: str) -> str:
    return value


@json_generator.register(abc.Mapping)
def _(value: Mapping) -> str:
    return json.dumps(value)
