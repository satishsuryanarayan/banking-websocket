from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class TransfersViewDTO(BaseDTO):
    @model_validator(mode="after")
    def validate_transfers_view_dto(self) -> Self:
        self.view = "TransfersView"
