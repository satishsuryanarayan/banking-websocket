from pydantic import BaseModel, model_validator
from typing_extensions import Self


class CreateCustomer(BaseModel):
    name: str

    @model_validator(mode="after")
    def validate_create_customer(self) -> Self:
        if not len(self.name.strip()) > 0:
            raise AssertionError("Name must not be empty")
        return self