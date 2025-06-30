from esmerald import Gateway
from lilya.middleware import DefineMiddleware

from banking.apps.bank.v1.view.bank import BankView
from banking.apps.bank.v1.view.users import UsersView
from banking.apps.bank.v1.view.utils.httpbasicauth import HTTPBasicAuth

route_patterns = [
    Gateway(handler=UsersView),
    Gateway(handler=BankView, middleware=[DefineMiddleware(HTTPBasicAuth)]),
]
