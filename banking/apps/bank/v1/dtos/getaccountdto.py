from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetAccountDTO(AccountsViewDTO):
    account_id: int

    def __init__(self, **data):
        super().__init__(**data)
        self.method = "get_account"
