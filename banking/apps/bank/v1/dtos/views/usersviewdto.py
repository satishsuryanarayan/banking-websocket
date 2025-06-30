from typing import Self

from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class UsersViewDTO(BaseDTO):
    @model_validator(mode="after")
    def validate_userto(self) -> Self:
        self.view = "UsersView"