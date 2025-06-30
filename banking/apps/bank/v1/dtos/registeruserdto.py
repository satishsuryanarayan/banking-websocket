from pydantic import EmailStr, model_validator
from typing_extensions import Self

from banking.apps.bank.v1.dtos.views.usersviewdto import UsersViewDTO


class RegisterUserDTO(UsersViewDTO):
    username: str
    password: str
    email: EmailStr

    @model_validator(mode="after")
    def validate_create_user(self) -> Self:
        if not len(self.username.strip()) >= 6:
            raise AssertionError("Username must be at least 6 characters")

        if not len(self.password.strip()) >= 10:
            raise AssertionError("Password must be at least 10 characters")

        self.method = "register_user"
        return self
