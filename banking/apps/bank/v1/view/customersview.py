from bank.datamodel.v1.dtos.createcustomer import CreateCustomerDTO
from bank.datamodel.v1.dtos.customer import CustomerDTO
from bank.datamodel.v1.dtos.getallcustomers import GetAllCustomersDTO
from bank.datamodel.v1.dtos.getcustomer import GetCustomerDTO
from esmerald import Stream, HTTPException
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.customers import CustomersController


class CustomersView:
    @classmethod
    async def get_all_customers(cls, param: GetAllCustomersDTO) -> Stream:
        try:
            return Stream(iterator=await CustomersController.get_all_customers(param.from_time, param.to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_customer(cls, param: GetCustomerDTO) -> CustomerDTO:
        try:
            return await CustomersController.get_customer(param.customer_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def create_customer(cls, param: CreateCustomerDTO) -> CustomerDTO:
        try:
            return await CustomersController.create_customer(param.name)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
