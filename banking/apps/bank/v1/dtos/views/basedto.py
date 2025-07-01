from pydantic import BaseModel


class BaseDTO(BaseModel):
    method: str = None
    view: str = None
