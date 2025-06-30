from datetime import datetime, timedelta
from typing import Self

from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.transfersviewdto import TransfersViewDTO


class GetAccountTransfersDTO(TransfersViewDTO):
    account_id: int
    from_time: datetime = datetime.now() - timedelta(days=7)
    to_time: datetime = datetime.now()

    @model_validator(mode="after")
    def validate_get_account_transfers(self) -> Self:
        self.method = "get_account_transfers"
