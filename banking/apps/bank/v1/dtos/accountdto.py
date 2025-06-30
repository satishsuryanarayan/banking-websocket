from datetime import datetime

from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class AccountDTO(AccountsViewDTO):
    id: int
    customer_id: int
    creation_time: datetime
