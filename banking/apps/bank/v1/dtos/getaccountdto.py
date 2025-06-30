from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetAccountDTO(AccountsViewDTO):
    account_id: int
