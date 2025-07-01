from decimal import Decimal

from pydantic import model_validator
from typing_extensions import Self

from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class CreateAccountDTO(AccountsViewDTO):
    customer_id: int
    amount: Decimal

    def __init__(self, **data):
        super().__init__(**data)
        self.method = "create_account"

    @model_validator(mode="after")
    def validate_create_account(self) -> Self:
        if not self.amount > 0:
            raise AssertionError("Amount must be positive")

        return self
