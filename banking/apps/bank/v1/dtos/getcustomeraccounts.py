from typing import Self

from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetCustomerAccountsDTO(AccountsViewDTO):
    customer_id: int

    @model_validator(mode="after")
    def validate_get_customer_accounts(self) -> Self:
        self.method = "get_customer_accounts"
