from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetAccountBalanceDTO(AccountsViewDTO):
    account_id: int
