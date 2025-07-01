from typing import Literal

from esmerald import settings
from esmerald.logging import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncEngine

from banking.apps.bank.v1.model.metadata import metadata


class Database:
    isolation_level = Literal["REPEATABLE READ", "SERIALIZABLE"]
    engines: dict[isolation_level, AsyncEngine] = dict()

    @classmethod
    def connect(cls, db_config: dict) -> None:
        cls.engines["SERIALIZABLE"] = create_async_engine(**db_config)
        cls.engines["REPEATABLE READ"] = cls.engines["SERIALIZABLE"].execution_options(
            isolation_level="REPEATABLE READ")

    @classmethod
    async def disconnect(cls) -> None:
        await cls.engines["SERIALIZABLE"].dispose()
        await cls.engines["REPEATABLE READ"].dispose()

    @classmethod
    async def get_connection(cls, isolation_level: isolation_level) -> AsyncConnection:
        return await cls.engines[isolation_level].connect()

    @classmethod
    async def init(cls) -> None:
        connection: AsyncConnection = await cls.get_connection("SERIALIZABLE")
        try:
            async with connection.begin():
                if settings.initdb:
                    await connection.run_sync(metadata.drop_all)
                try:
                    await connection.run_sync(metadata.create_all)
                except Exception as e:
                    logger.error("Exception occurred when initializing database:", e, exc_info=True)
            logger.info("Database initialized.")
        finally:
            await connection.close()
