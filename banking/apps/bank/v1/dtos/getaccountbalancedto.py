from typing import Self

from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetAccountBalanceDTO(AccountsViewDTO):
    account_id: int

    @model_validator(mode="after")
    def validate_get_account_balance(self) -> Self:
        self.method = "get_account_balance"
