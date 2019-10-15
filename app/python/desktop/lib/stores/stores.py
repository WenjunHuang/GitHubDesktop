from abc import ABC
from typing import *


class IDataStore(ABC):
    def set_item(self, key: str, value: str) -> None:
        pass

    def get_item(self, key: str) -> Optional[str]:
        pass


class ISecureStore(ABC):
    async def set_item(self, key: str, login: str, value: str) -> None:
        pass

    async def get_item(self, key: str, login: str) -> Optional[str]:
        pass

    async def delete_item(self, key: str, login: str) -> Optional[bool]:
        pass
