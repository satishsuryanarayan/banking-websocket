from datetime import datetime, timedelta
from typing import Self

from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetAllAccountsDTO(AccountsViewDTO):
    from_time: datetime = datetime.now() - timedelta(days=7)
    to_time: datetime = datetime.now()

    @model_validator(mode="after")
    def validate_get_all_accounts(self) -> Self:
        self.method = "get_all_accounts"
