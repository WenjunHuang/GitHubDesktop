from dataclasses import dataclass
from typing import Optional

from PyQt5.QtQml import QJSValue


@dataclass
class LoadAccountRepositoryEvent:
    endpoint: str
    token: str

    @classmethod
    def from_jsvalue(cls, js_props: QJSValue):
        token = js_props.property('token').toString()
        endpoint = js_props.property('endpoint').toString()
        return LoadAccountRepositoryEvent(token=token, endpoint=endpoint)
