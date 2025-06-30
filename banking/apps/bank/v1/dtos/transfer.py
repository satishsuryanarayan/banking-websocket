from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Transfer(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    time: datetime
