from datetime import datetime, timedelta

from banking.apps.bank.v1.dtos.views.transfersviewdto import TransfersViewDTO


class GetAccountTransfersDTO(TransfersViewDTO):
    account_id: int
    from_time: datetime = datetime.now() - timedelta(days=7)
    to_time: datetime = datetime.now()
