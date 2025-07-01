from typing import Any

from esmerald import APIView, Stream, WebSocket, websocket
from esmerald.logging import logger
from pydantic import BaseModel

from banking.apps.bank.v1.dtos.errordto import ErrorDTO
import importlib

class BankView(APIView):
    path = "/bank"

    @websocket(path="/")
    async def handle(self, socket: WebSocket) -> None:
        await socket.accept()
        while True:
            dto = await socket.receive_json()
            if "view" in dto and "method" in dto:
                try:
                    module, cls = dto["view"].rsplit(".", 1)
                    view_cls: Any = getattr(importlib.import_module(module), cls)
                    logger.debug("View class: " + str(view_cls))
                    method_ref = getattr(view_cls, dto["method"])
                    logger.debug("View method: " + str(method_ref))
                    schema_type: BaseModel = method_ref.__annotations__["dto"]
                    logger.debug("Schema type: " + str(schema_type))
                    return_type: Any = method_ref.__annotations__["return"]
                    logger.debug("Return type: " + str(return_type))
                    if issubclass(return_type, BaseModel):
                        logger.info("Return type: " + str(return_type))
                        logger.info("Handling BaseModel...")
                        response: BaseModel = await method_ref(schema_type.model_validate(dto))
                        await socket.send_text(response.model_dump_json())
                    elif issubclass(return_type, Stream):
                        logger.info("Return type: " + str(return_type))
                        logger.info("Handling Stream...")
                        response: Stream = await method_ref(schema_type.model_validate(dto))
                        async for value in response.iterator():
                            value_type = type(value)
                            logger.info(f"Type of value is {value_type}")
                            await socket.send_text(value)
                    else:
                        logger.debug("Return type: " + str(return_type))
                        raise RuntimeError("Unhandled return type: " + str(return_type))
                except Exception as err:
                    logger.info("Exception in handle()", err, exc_info=True)
                    response: ErrorDTO = ErrorDTO(detail=repr(err))
                    await socket.send_text(response.model_dump_json())
            else:
                error: ErrorDTO = ErrorDTO(detail=dto["Invalid DTO"])
                await socket.send_text(error.model_dump_json())
