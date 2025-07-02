from pydantic import BaseModel


class ErrorDTO(BaseModel):
    detail: str

    def __init__(self, **data):
        super().__init__(**data)
