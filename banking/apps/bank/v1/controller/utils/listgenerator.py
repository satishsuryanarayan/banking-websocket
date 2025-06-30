from typing import AsyncGenerator, Type

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncMappingResult

chunk_size = 100


# Generator to stream result list
async def list_generator(cursor: AsyncMappingResult, connection: AsyncConnection, schema: Type[BaseModel],
                         size=chunk_size) -> AsyncGenerator[str]:
    try:
        yield "["
        results = await cursor.fetchmany(size=size)
        while results:
            serialized_data = []
            for row in results:
                instance: BaseModel = schema.model_validate(row)
                serialized_data.append(instance.model_dump_json())
            yield ", ".join(serialized_data)
            results = await cursor.fetchmany(size=size)
            if results:
                yield ", "
        yield "]"
    finally:
        await cursor.close()
        await connection.close()
