from dataclasses import is_dataclass, fields
from enum import Enum
from functools import singledispatch
from typing import Optional, Any, Iterable
from PyQt5.QtQml import QJSValue
from datetime import datetime, timedelta, timezone
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
@to_jsobject.register(tuple)
def _(data: Iterable[Any]):
    js_array = get_qml_engine().newArray()
    for idx, v in enumerate(data):
        result = to_jsobject(v)
        js_array.setProperty(idx, result)
    return js_array


def utc_now_with_timezone() -> datetime:
    return datetime.now().astimezone(timezone.utc)


def local_now_with_timezone() -> datetime:
    return datetime.now().astimezone()


def to_utc(dt: datetime) -> datetime:
    assert dt.tzinfo
    utc_time = dt - dt.tzinfo.utcoffset(None)
    return utc_time.replace(tzinfo=timezone.utc)


def utc_to_local(dt: datetime) -> datetime:
    assert (dt.tzinfo and dt.tzinfo == timezone.utc)
    return dt.astimezone()


def timestamp_seconds(dt: datetime) -> int:
    assert dt.tzinfo
    return int(dt.timestamp())


def from_timestamp_to_local(timestamp: int) -> datetime:
    return utc_to_local(datetime.fromtimestamp(timestamp, tz=timezone.utc))
