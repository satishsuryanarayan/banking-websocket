from datetime import datetime
from typing import Optional

from esmerald import APIView, Stream, HTTPException
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.handlers import get, post
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.customers import CustomersController
from banking.apps.bank.v1.dtos.createcustomer import CreateCustomer
from banking.apps.bank.v1.dtos.customer import Customer
from banking.apps.bank.v1.dtos.error import Error


class CustomersView(APIView):
    path = "/customers"

    @get(
        path="/",
        tags=["Customers"],
        summary="Get customers",
        description="Get all customers created between from_time and to_time",
        responses={
            200: OpenAPIResponse(model=[Customer], description="Customer list"),
            400: OpenAPIResponse(model=Error, description="Bad response"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_all_customers(self, from_time: Optional[datetime] = None, to_time: Optional[datetime] = None) -> Stream:
        try:
            return Stream(iterator=await CustomersController.get_all_customers(from_time, to_time))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @get(
        path="/{customer_id}",
        tags=["Customers"],
        summary="Get customer",
        description="Get customer details by customer ID",
        responses={
            200: OpenAPIResponse(model=Customer, description="Customer details"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def get_customer(self, customer_id: int) -> Customer:
        try:
            return await CustomersController.get_customer(customer_id)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @post(
        path="/",
        tags=["Customers"],
        summary="Create a customer",
        description="Creates a new bank customer",
        responses={
            201: OpenAPIResponse(model=Customer, description="Newly created customer"),
            400: OpenAPIResponse(model=Error, description="Bad request"),
            401: OpenAPIResponse(model=Error, description="Not authorized"),
        }
    )
    async def create_customer(self, customer: CreateCustomer) -> Customer:
        try:
            return await CustomersController.create_customer(customer)
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
