from datetime import datetime, timedelta

from banking.apps.bank.v1.dtos.views.customersviewdto import CustomersViewDTO


class GetAllCustomersDTO(CustomersViewDTO):
    from_time: datetime = datetime.now() - timedelta(days=7)
    to_time: datetime = datetime.now()

    def __init__(self, **data):
        super().__init__(**data)
        self.method = "get_all_customers"
