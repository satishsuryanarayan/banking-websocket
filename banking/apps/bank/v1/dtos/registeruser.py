from pydantic import BaseModel, EmailStr, model_validator
from typing_extensions import Self


class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr

    @model_validator(mode="after")
    def validate_create_user(self) -> Self:
        if not len(self.username.strip()) >= 6:
            raise AssertionError("Username must be at least 6 characters")

        if not len(self.password.strip()) >= 10:
            raise AssertionError("Password must be at least 10 characters")
        return self
