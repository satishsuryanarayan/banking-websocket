from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class AccountsViewDTO(BaseDTO):
    def __init__(self, **data):
        super().__init__(**data)
        self.view = "banking.apps.bank.v1.view.accountsview.AccountsView"
