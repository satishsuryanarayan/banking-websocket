from banking.apps.bank.v1.dtos.views.basedto import BaseDTO


class UsersViewDTO(BaseDTO):
    def __init__(self, **data):
        super().__init__(**data)
        self.view = "banking.apps.bank.v1.view.usersview.UsersView"
