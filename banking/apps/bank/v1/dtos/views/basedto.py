from pydantic import BaseModel, model_validator
from typing_extensions import Self


class BaseDTO(BaseModel):
    method: str = None
    view: str = None
