from datetime import datetime

from banking.apps.bank.v1.dtos.views.customersviewdto import CustomersViewDTO


class CustomerDTO(CustomersViewDTO):
    id: int
    name: str
    creation_time: datetime

    def __init__(self, **data):
        super().__init__(**data)
