from dataclasses import dataclass

from PyQt5.QtQml import QJSValue


@dataclass
class LoadAccountRepositoriesEvent:
    @classmethod
    def from_jsvalue(cls, js_props: QJSValue):
        return LoadAccountRepositoriesEvent()
