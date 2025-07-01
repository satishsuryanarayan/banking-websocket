from esmerald import APIView, Stream, WebSocket, websocket
from esmerald.logging import logger
from pydantic import BaseModel

import banking.apps.bank.v1.view as view
from banking.apps.bank.v1.dtos.errordto import ErrorDTO


class BankView(APIView):
    path = "/bank"

    @websocket(path="/")
    async def handle(self, socket: WebSocket) -> None:
        await socket.accept()
        while True:
            msg = await socket.receive_json()
            if "view" in msg and "method" in msg:
                try:
                    view_cls = getattr(view, msg["view"])
                    logger.info("View class: " + str(view_cls))
                    method_ref = getattr(view_cls, msg["method"])
                    logger.info("View method: " + str(method_ref))
                    schema_type = method_ref.__annotations__["dto"]
                    logger.info("Schema type: " + str(schema_type))
                    return_type = method_ref.__annotations__["return"]
                    logger.info("Return type: " + str(return_type))
                    if issubclass(return_type, BaseModel):
                        response: BaseModel = await method_ref(schema_type.model_validate(msg))
                        await socket.send_json(response.model_dump_json())
                    elif issubclass(return_type, Stream):
                        response: Stream = await method_ref(schema_type.model_validate(msg))
                        async for value in response.iterator:
                            await socket.send_text(value)
                    else:
                        raise RuntimeError("Unhandled return type: " + str(return_type))
                except Exception as err:
                    response: ErrorDTO = ErrorDTO(detail=repr(err))
                    await socket.send_json(response.model_dump_json())
            else:
                error: ErrorDTO = ErrorDTO(detail=msg["Invalid DTO"])
                await socket.send_json(error)
