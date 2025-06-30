from decimal import Decimal

from pydantic import BaseModel, model_validator
from typing_extensions import Self


class CreateTransfer(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal

    @model_validator(mode="after")
    def validate_create_transfer(self) -> Self:
        if not self.amount > 0:
            raise AssertionError("Cannot transfer negative amount")
        if self.from_account_id == self.to_account_id:
            raise AssertionError("Cannot transfer money to same account")

        return self
