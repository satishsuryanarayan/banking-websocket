from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class GetCustomerAccountsDTO(AccountsViewDTO):
    customer_id: int
