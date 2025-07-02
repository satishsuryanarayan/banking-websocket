from pydantic import BaseModel


class BaseDTO(BaseModel):
    method: str = None
    view: str = None

    def __init__(self, **data):
        super().__init__(**data)
