from datetime import datetime
from decimal import Decimal

from banking.apps.bank.v1.dtos.views.accountsviewdto import AccountsViewDTO


class BalanceDTO(AccountsViewDTO):
    account_id: int
    amount: Decimal
    last_updated_time: datetime

    def __init__(self, **data):
        super().__init__(**data)
