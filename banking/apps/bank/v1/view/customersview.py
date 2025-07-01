from esmerald import Stream, HTTPException
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.customers import CustomersController
from banking.apps.bank.v1.dtos.createcustomerdto import CreateCustomerDTO
from banking.apps.bank.v1.dtos.customerdto import CustomerDTO
from banking.apps.bank.v1.dtos.getallcustomersdto import GetAllCustomersDTO
from banking.apps.bank.v1.dtos.getcustomerdto import GetCustomerDTO


class CustomersView:
    @classmethod
    async def get_all_customers(cls, dto: GetAllCustomersDTO) -> Stream:
        try:
            return Stream(iterator=await CustomersController.get_all_customers(dto.from_time, dto.to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_customer(cls, dto: GetCustomerDTO) -> CustomerDTO:
        try:
            return await CustomersController.get_customer(dto.customer_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def create_customer(cls, dto: CreateCustomerDTO) -> CustomerDTO:
        try:
            return await CustomersController.create_customer(dto.name)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
