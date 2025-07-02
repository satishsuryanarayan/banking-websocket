import importlib
from typing import Type

from esmerald import APIView, Stream, View, WebSocket, websocket
from esmerald.logging import logger

from banking.apps.bank.v1.dtos.errordto import ErrorDTO
from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class BankView(View):
    path = "/bank"


    @websocket(path="/")
    async def handle(self, socket: WebSocket) -> None:
        eom: str = "<.-.-.>"
        await socket.accept()
        while True:
            dto = await socket.receive_json()
            if "view" in dto and "method" in dto:
                try:
                    module, cls = dto["view"].rsplit(".", 1)
                    view_type: Type[object | APIView] = getattr(importlib.import_module(module), cls)
                    method_ref = getattr(view_type, dto["method"])
                    schema_type: Type[BaseDTO] = method_ref.__annotations__["param"]
                    return_type: Type[BaseDTO | Stream] = method_ref.__annotations__["return"]
                    if issubclass(return_type, BaseDTO):
                        logger.debug("Handling BaseDTO...")
                        response: BaseDTO = await method_ref(schema_type.model_validate(dto))
                        await socket.send_text(response.model_dump_json())
                    elif issubclass(return_type, Stream):
                        logger.debug("Handling Stream...")
                        response: Stream = await method_ref(schema_type.model_validate(dto))
                        async for value in response.iterator:
                            await socket.send_text(value)
                        await socket.send_text(eom)
                    else:
                        logger.error("Unhandled return type: " + str(return_type))
                        raise RuntimeError("Unhandled return type: " + str(return_type))
                except Exception as err:
                    logger.info("Exception in websocket handler", err, exc_info=True)
                    response: ErrorDTO = ErrorDTO(detail=repr(err))
                    await socket.send_text(response.model_dump_json())
            else:
                error: ErrorDTO = ErrorDTO(detail=dto["Invalid DTO"])
                await socket.send_text(error.model_dump_json())
