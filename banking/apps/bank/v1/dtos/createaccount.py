from decimal import Decimal

from pydantic import BaseModel, model_validator
from typing_extensions import Self


class CreateAccount(BaseModel):
    customer_id: int
    amount: Decimal

    @model_validator(mode="after")
    def validate_create_account(self) -> Self:
        if not self.amount > 0:
            raise AssertionError("Amount must be positive")

        return self