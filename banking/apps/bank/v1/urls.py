from esmerald import Gateway, WebSocketGateway
from lilya.middleware import DefineMiddleware

from banking.apps.bank.v1.view.bankview import BankView
from banking.apps.bank.v1.view.usersview import UsersView
from banking.apps.bank.v1.view.utils.httpbasicauth import HTTPBasicAuth

route_patterns = [
    Gateway(handler=UsersView),
    WebSocketGateway(handler=BankView, middleware=[DefineMiddleware(HTTPBasicAuth)]),
]
