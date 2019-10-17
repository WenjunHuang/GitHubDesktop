from typing import Optional

import keyring

from .stores import ISecureStore


class TokenStore(ISecureStore):
    async def set_item(self, key: str, login: str, value: str) -> None:
        keyring.set_password(key, login, value)

    async def get_item(self, key: str, login: str) -> Optional[str]:
        return keyring.get_password(key, login)

    async def delete_item(self, key: str, login: str) -> Optional[bool]:
        keyring.delete_password(key, login)
