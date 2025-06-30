from datetime import datetime

from pydantic import BaseModel


class Customer(BaseModel):
    id: int
    name: str
    creation_time: datetime
