from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class AccountsViewDTO(BaseDTO):
    @model_validator(mode="after")
    def validate_accountdto(self) -> Self:
        self.view = "AccountsView"