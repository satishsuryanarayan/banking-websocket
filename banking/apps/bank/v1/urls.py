from esmerald import Gateway
from lilya.middleware import DefineMiddleware

from banking.apps.bank.v1.view.accounts import AccountsView
from banking.apps.bank.v1.view.customers import CustomersView
from banking.apps.bank.v1.view.transfers import TransfersView
from banking.apps.bank.v1.view.users import UsersView
from banking.apps.bank.v1.view.utils.httpbasicauth import HTTPBasicAuth

route_patterns = [
    Gateway(handler=UsersView),
    Gateway(handler=CustomersView, middleware=[DefineMiddleware(HTTPBasicAuth)]),
    Gateway(handler=AccountsView, middleware=[DefineMiddleware(HTTPBasicAuth)]),
    Gateway(handler=TransfersView, middleware=[DefineMiddleware(HTTPBasicAuth)]),
]
