from datetime import datetime
from typing import Optional

from esmerald.logging import logger
from esmerald import APIView, Stream, HTTPException
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.handlers import get, post
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.accounts import AccountsController
from banking.apps.bank.v1.dtos.account import Account
from banking.apps.bank.v1.dtos.balance import Balance
from banking.apps.bank.v1.dtos.createaccount import CreateAccount
from banking.apps.bank.v1.dtos.error import Error


class AccountsView(APIView):
    path = "/accounts"

    @get(
        path="/",
        tags=["Accounts"],
        summary="Get accounts",
        description="Get all accounts created between from_time and to_time",
        responses={
            200: OpenAPIResponse(model=[Account], description="Account list"),
            400: OpenAPIResponse(model=Error, description="Bad response"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_all_accounts(self, from_time: Optional[datetime] = None, to_time: Optional[datetime] = None) -> Stream:
        try:
            logger.debug(str(from_time))
            logger.debug(str(to_time))
            return Stream(iterator=await AccountsController.get_all_accounts(from_time, to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @get(
        path="/customer/{customer_id}",
        tags=["Accounts"],
        summary="Get accounts for customer",
        description="Get all accounts for customer by customer ID",
        responses={
            200: OpenAPIResponse(model=[Account], description="Account list for customer"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_customer_accounts(self, customer_id: int) -> Stream:
        try:
            return Stream(iterator=await AccountsController.get_customer_accounts(customer_id))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @post(
        path="/",
        tags=["Accounts"],
        summary="Create an account",
        description="Creates a new account with initial balance for an existing customer",
        responses={
            201: OpenAPIResponse(model=Account, description="Newly created account"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def create_customer(self, account: CreateAccount) -> Account:
        try:
            return await AccountsController.create_account(account)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @get(
        path="/{account_id}",
        tags=["Accounts"],
        summary="Get account",
        description="Get account by account ID",
        responses={
            200: OpenAPIResponse(model=Account, description="Account data"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_account(self, account_id: int) -> Account:
        try:
            return await AccountsController.get_account(account_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @get(
        path="/balance/{account_id}",
        tags=["Accounts"],
        summary="Get account balance",
        description="Get account balance by account ID",
        responses={
            200: OpenAPIResponse(model=Balance, description="Account balance"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_account_balance(self, account_id: int) -> Balance:
        try:
            return await AccountsController.get_account_balance(account_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
