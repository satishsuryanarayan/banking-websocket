from typing import Type

from bank.datamodel.v1.dtos.error import ErrorDTO
from bank.datamodel.v1.dtos.views.base import BaseDTO
from bank.protocol.message import Message
from esmerald import Stream, View, WebSocket, websocket
from esmerald.logging import logger

from banking.apps.bank.v1.view.accountsview import AccountsView
from banking.apps.bank.v1.view.customersview import CustomersView
from banking.apps.bank.v1.view.transfersview import TransfersView
from banking.apps.bank.v1.view.usersview import UsersView


class BankView(View):
    path = "/bank"

    views: dict[str, Type[View]] = {
        "AccountsView": AccountsView,
        "CustomersView": CustomersView,
        "TransfersView": TransfersView,
        "UsersView": UsersView
    }

    @websocket(path="/")
    async def handle(self, socket: WebSocket) -> None:
        await socket.accept()
        while True:
            try:
                dto: BaseDTO = await socket.receive_json()
                try:
                    view: str = dto["view"]
                    view_type: Type[View] = BankView.views.get(view)
                    if view_type is None:
                        error: ErrorDTO = ErrorDTO(detail="Invalid view " + view)
                        await socket.send_text(error.model_dump_json(exclude_none=True))
                    else:
                        method_ref = getattr(view_type, dto["method"])
                        schema_type: Type[BaseDTO] = method_ref.__annotations__["param"]
                        return_type: Type[BaseDTO | Stream] = method_ref.__annotations__["return"]
                        if issubclass(return_type, BaseDTO):
                            logger.debug("Handling BaseDTO...")
                            response: BaseDTO = await method_ref(schema_type.model_validate(dto))
                            await socket.send_text(response.model_dump_json(exclude_none=True))
                        elif issubclass(return_type, Stream):
                            logger.debug("Handling Stream...")
                            response: Stream = await method_ref(schema_type.model_validate(dto))
                            async for value in response.iterator:
                                await socket.send_text(value)
                            await socket.send_text(Message.END)
                        else:
                            logger.error("Unhandled return type: " + str(return_type))
                            raise RuntimeError("Unhandled return type: " + str(return_type))
                except Exception as err:
                    logger.info("Exception in websocket handler", err, exc_info=True)
                    response: ErrorDTO = ErrorDTO(detail=repr(err))
                    await socket.send_text(response.model_dump_json(exclude_none=True))
            except Exception as err:
                logger.info("Error receiving dto payload", err, exc_info=True)
                error: ErrorDTO = ErrorDTO(detail=err.__str__())
                await socket.send_text(error.model_dump_json(exclude_none=True))
