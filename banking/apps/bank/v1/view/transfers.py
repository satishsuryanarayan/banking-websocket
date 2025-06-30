from esmerald import Stream, HTTPException
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.transfers import TransfersController
from banking.apps.bank.v1.dtos.createtransferdto import CreateTransferDTO
from banking.apps.bank.v1.dtos.getaccounttransfersdto import GetAccountTransfersDTO
from banking.apps.bank.v1.dtos.transferdto import TransferDTO


class TransfersView:
    @classmethod
    async def get_account_transfers(cls, dto: GetAccountTransfersDTO) -> Stream:
        try:
            return Stream(
                iterator=await TransfersController.get_account_transfers(dto.account_id, dto.from_time, dto.to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def create_transfer(cls, dto: CreateTransferDTO) -> TransferDTO:
        try:
            return await TransfersController.create_transfer(dto.from_account_id, dto.account_id, dto.amount)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
