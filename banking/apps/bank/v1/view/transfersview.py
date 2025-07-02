from bank.datamodel.v1.dtos.createtransfer import CreateTransferDTO
from bank.datamodel.v1.dtos.getaccounttransfers import GetAccountTransfersDTO
from bank.datamodel.v1.dtos.transfer import TransferDTO
from esmerald import Stream, HTTPException
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.transfers import TransfersController


class TransfersView:
    @classmethod
    async def get_account_transfers(cls, param: GetAccountTransfersDTO) -> Stream:
        try:
            return Stream(
                iterator=await TransfersController.get_account_transfers(param.account_id, param.from_time,
                                                                         param.to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def create_transfer(cls, param: CreateTransferDTO) -> TransferDTO:
        try:
            return await TransfersController.create_transfer(param.from_account_id, param.to_account_id, param.amount)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
