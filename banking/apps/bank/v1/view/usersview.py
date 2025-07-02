from bank.datamodel.v1.dtos.error import ErrorDTO
from bank.datamodel.v1.dtos.registeruser import RegisterUserDTO
from bank.datamodel.v1.dtos.user import UserDTO
from esmerald import APIView, HTTPException
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.handlers import post
from lilya.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from banking.apps.bank.v1.controller.users import UsersController


class UsersView(APIView):
    path = "/users"

    @post(
        path="/",
        tags=["Users"],
        summary="Register a user",
        description="Registers a new user",
        responses={
            201: OpenAPIResponse(model=UserDTO, description="Newly registered user"),
            400: OpenAPIResponse(model=ErrorDTO, description="Bad request"),
            401: OpenAPIResponse(model=ErrorDTO, description="Not authorized"),
        }
    )
    async def register_user(self, param: RegisterUserDTO) -> UserDTO:
        try:
            return await UsersController.register_user(param.username, param.password, str(param.email))
        except AssertionError as ae:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ae))
        except ResourceWarning as rw:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(rw))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
