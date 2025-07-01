from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class CustomersViewDTO(BaseDTO):
    def __init__(self, **data):
        super().__init__(**data)
        self.view = "banking.apps.bank.v1.view.customersview.CustomersView"
