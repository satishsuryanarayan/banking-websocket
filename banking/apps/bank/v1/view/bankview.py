from esmerald import APIView, WebSocket, websocket

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
                    method_ref = getattr(view_cls, msg["method"])
                    schema_type = method_ref.__annotations__["dto"]
                    response = await method_ref(schema_type.model_validate(msg))
                except Exception as err:
                    response = ErrorDTO(detail=repr(err))

                await socket.send_json(response)
            else:
                error: ErrorDTO = ErrorDTO(detail=msg["Invalid DTO"])
                await socket.send_json(error)
