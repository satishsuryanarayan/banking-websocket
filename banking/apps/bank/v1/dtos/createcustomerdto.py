from pydantic import model_validator
from typing_extensions import Self

from banking.apps.bank.v1.dtos.views.customersviewdto import CustomersViewDTO


class CreateCustomerDTO(CustomersViewDTO):
    name: str

    @model_validator(mode="after")
    def validate_create_customer(self) -> Self:
        if not len(self.name.strip()) > 0:
            raise AssertionError("Name must not be empty")

        self.method = "create_customer"
        return self
