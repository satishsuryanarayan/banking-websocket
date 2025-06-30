from datetime import datetime, timedelta
from typing import Optional

from esmerald import APIView, Stream, HTTPException
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.handlers import get, post
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.transfers import TransfersController
from banking.apps.bank.v1.dtos.createtransfer import CreateTransfer
from banking.apps.bank.v1.dtos.error import Error
from banking.apps.bank.v1.dtos.transfer import Transfer


class TransfersView(APIView):
    path = "/transfers"

    @get(
        path="/account/{account_id}",
        tags=["Transfers"],
        summary="Get account transfers",
        description="Get all transfers between from_time and to_time for account by account ID",
        responses={
            200: OpenAPIResponse(model=[Transfer], description="Account transfer list"),
            400: OpenAPIResponse(model=Error, description="Bad response"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_account_transfers(self, account_id: int,
                                    from_time: Optional[datetime] = (datetime.now() - timedelta(days=7)),
                                    to_time: Optional[datetime] = datetime.now()) -> Stream:
        try:
            return Stream(iterator=await TransfersController.get_account_transfers(account_id, from_time, to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @post(
        path="/",
        tags=["Transfers"],
        summary="Create a transfer",
        description="Creates a new transfer between existing accounts",
        responses={
            201: OpenAPIResponse(model=Transfer, description="Newly created transfer"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def create_transfer(self, transfer: CreateTransfer) -> Transfer:
        try:
            return await TransfersController.create_transfer(transfer)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
