from typing import Self

from pydantic import model_validator

from banking.apps.bank.v1.dtos.views.customersviewdto import CustomersViewDTO


class GetCustomerDTO(CustomersViewDTO):
    customer_id: int

    @model_validator(mode="after")
    def validate_customer(self) -> Self:
        self.method = "get_customer"
