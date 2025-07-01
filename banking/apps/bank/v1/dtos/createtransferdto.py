from decimal import Decimal

from pydantic import model_validator
from typing_extensions import Self

from banking.apps.bank.v1.dtos.views.transfersviewdto import TransfersViewDTO


class CreateTransferDTO(TransfersViewDTO):
    from_account_id: int
    to_account_id: int
    amount: Decimal

    def __init__(self, **data):
        super().__init__(**data)
        self.method = "create_transfer"

    @model_validator(mode="after")
    def validate_create_transfer(self) -> Self:
        if not self.amount > 0:
            raise AssertionError("Cannot transfer negative amount")
        if self.from_account_id == self.to_account_id:
            raise AssertionError("Cannot transfer money to same account")

        return self
