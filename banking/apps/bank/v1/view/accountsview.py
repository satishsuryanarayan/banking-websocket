from esmerald import Stream, HTTPException
from esmerald.logging import logger
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.accounts import AccountsController
from banking.apps.bank.v1.dtos.accountdto import AccountDTO
from banking.apps.bank.v1.dtos.balancedto import BalanceDTO
from banking.apps.bank.v1.dtos.createaccountdto import CreateAccountDTO
from banking.apps.bank.v1.dtos.getaccountbalancedto import GetAccountBalanceDTO
from banking.apps.bank.v1.dtos.getaccountdto import GetAccountDTO
from banking.apps.bank.v1.dtos.getallaccountsdto import GetAllAccountsDTO
from banking.apps.bank.v1.dtos.getcustomeraccounts import GetCustomerAccountsDTO


class AccountsView:
    @classmethod
    async def get_all_accounts(cls, dto: GetAllAccountsDTO) -> Stream:
        try:
            logger.debug(str(dto.from_time))
            logger.debug(str(dto.to_time))
            return Stream(iterator=await AccountsController.get_all_accounts(dto.from_time, dto.to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_customer_accounts(cls, dto: GetCustomerAccountsDTO) -> Stream:
        try:
            return Stream(iterator=await AccountsController.get_customer_accounts(dto.customer_id))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def create_account(cls, dto: CreateAccountDTO) -> AccountDTO:
        try:
            return await AccountsController.create_account(dto.customer_id, dto.amount)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_account(cls, dto: GetAccountDTO) -> AccountDTO:
        try:
            return await AccountsController.get_account(dto.account_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_account_balance(cls, dto: GetAccountBalanceDTO) -> BalanceDTO:
        try:
            return await AccountsController.get_account_balance(dto.account_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
