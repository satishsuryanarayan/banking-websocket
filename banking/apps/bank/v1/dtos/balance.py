from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Balance(BaseModel):
    account_id: int
    amount: Decimal
    last_updated_time: datetime
