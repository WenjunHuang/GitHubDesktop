from dataclasses import is_dataclass, fields
from enum import Enum
from functools import singledispatch
from typing import Optional, Any

from PyQt5.QtQml import QJSValue

from desktop.lib.static import get_qml_engine


@singledispatch
def to_jsobject(data) -> Optional[Any]:
    if not data:
        return QJSValue(QJSValue.NullValue)
    elif is_dataclass(data):
        js_obj = get_qml_engine().newObject()
        for f in fields(data):
            v = getattr(data, f.name)
            v = to_jsobject(v)
            js_obj.setProperty(f.name, v)
        return js_obj
    else:
        raise Exception(f'unsupported object {data}')


@to_jsobject.register(str)
@to_jsobject.register(int)
@to_jsobject.register(bool)
@to_jsobject.register(float)
def _(data):
    return QJSValue(data)


@to_jsobject.register(Enum)
def _(data):
    return QJSValue(data.value)


@to_jsobject.register(list)
def _(data: list):
    js_array = get_qml_engine().newArray()
    for idx, v in enumerate(data):
        result = to_jsobject(v)
        js_array.setProperty(idx, result)
    return js_array
