from typing import Any

from esmerald import APIView, Stream, WebSocket, websocket
from esmerald.logging import logger
from pydantic import BaseModel

from banking.apps.bank.v1.dtos.errordto import ErrorDTO
import importlib

class BankView(APIView):
    path = "/bank"
    module = importlib.import_module("banking.apps.bank.v1.view")

    @websocket(path="/")
    async def handle(self, socket: WebSocket) -> None:
        await socket.accept()
        while True:
            dto = await socket.receive_json()
            if "view" in dto and "method" in dto:
                try:
                    view_cls: APIView = getattr(self.module, dto["view"])
                    logger.info("View class: " + str(view_cls))
                    method_ref = getattr(view_cls, dto["method"])
                    logger.info("View method: " + str(method_ref))
                    schema_type: BaseModel = method_ref.__annotations__["dto"]
                    logger.info("Schema type: " + str(schema_type))
                    return_type: Any = method_ref.__annotations__["return"]
                    logger.info("Return type: " + str(return_type))
                    if issubclass(return_type, BaseModel):
                        response: BaseModel = await method_ref(schema_type.model_validate(dto))
                        await socket.send_json(response.model_dump_json())
                    elif issubclass(return_type, Stream):
                        response: Stream = await method_ref(schema_type.model_validate(dto))
                        async for value in response.iterator:
                            await socket.send_text(value)
                    else:
                        raise RuntimeError("Unhandled return type: " + str(return_type))
                except Exception as err:
                    response: ErrorDTO = ErrorDTO(detail=repr(err))
                    await socket.send_json(response.model_dump_json())
            else:
                error: ErrorDTO = ErrorDTO(detail=dto["Invalid DTO"])
                await socket.send_json(error)
