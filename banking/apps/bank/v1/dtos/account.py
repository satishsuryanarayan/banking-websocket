from datetime import datetime

from pydantic import BaseModel


class Account(BaseModel):
    id: int
    customer_id: int
    creation_time: datetime
