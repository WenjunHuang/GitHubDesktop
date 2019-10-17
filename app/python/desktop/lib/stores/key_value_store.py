from typing import Optional

from aiosqlite import Connection
from pypika import Table, SQLLiteQuery as Query, Parameter

from desktop.lib.stores import IKeyValueStore

KeyStringValueTable = Table('t_key_value_string')


class KeyValueStore(IKeyValueStore):
    def __init__(self, database: Connection):
        self.database = database

    async def set_item(self, key: str, value: str) -> None:
        replace = Query.into(KeyStringValueTable) \
            .columns(KeyStringValueTable.key, KeyStringValueTable.value) \
            .replace(Parameter('?'), Parameter('?'))
        await self.database.execute_insert(replace.get_sql(), (key, value))
        await self.database.commit()

    async def get_item(self, key: str) -> Optional[str]:
        q = Query.from_(KeyStringValueTable).select(KeyStringValueTable.value).where(KeyStringValueTable.key == key)
        cursor = await self.database.execute(q.get_sql())
        result = await cursor.fetchone()
        if not result:
            return None
        else:
            return result['value']
