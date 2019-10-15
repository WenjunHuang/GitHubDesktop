import logging
import getpass
import os
from functools import singledispatch
from io import BytesIO, TextIOWrapper

from aiofile import AIOFile, Reader


def with_logger(cls):
    """Class decorator to add a logger to a class."""
    attr_name = '_logger'
    cls_name = cls.__qualname__
    module = cls.__module__
    if module is not None:
        cls_name = module + '.' + cls_name
    else:
        raise AssertionError
    setattr(cls, attr_name, logging.getLogger(cls_name))
    return cls


def get_machine_username() -> str:
    return getpass.getuser()


async def read_text_file_content(file_path: str, encoding: str = 'utf-8'):
    async with AIOFile(file_path, 'rb') as afp:
        reader = Reader(afp, chunk_size=1024)
        with BytesIO() as b:
            async for chunk in reader:
                b.write(chunk)
            b.seek(0)
            return b.read().decode(encoding)
