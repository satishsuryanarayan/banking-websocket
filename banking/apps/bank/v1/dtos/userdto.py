from pydantic import EmailStr

from banking.apps.bank.v1.dtos.views.usersviewdto import UsersViewDTO


class UserDTO(UsersViewDTO):
    username: str
    password: str
    email: EmailStr
