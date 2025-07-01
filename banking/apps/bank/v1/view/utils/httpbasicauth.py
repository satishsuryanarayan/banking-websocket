import base64
import binascii

from esmerald.exceptions import NotAuthorized
from esmerald.logging import logger
from esmerald.middleware import BaseAuthMiddleware
from esmerald.middleware.authentication import AuthResult
from lilya._internal._connection import Connection

from banking.apps.bank.v1.controller.users import UsersController


class HTTPBasicAuth(BaseAuthMiddleware):
    def __init__(self, app: "ASGIApp"):
        super().__init__(app)
        self.app = app

    async def authenticate(self, request: Connection) -> AuthResult:
        logger.info("Authenticating...")
        logger.info(str(request.headers))
        auth_header = request.headers.get("authorization")
        logger.info(str(auth_header))

        if not auth_header or not auth_header.startswith("Basic "):
            logger.info("No authorization header")
            raise NotAuthorized("Invalid user credentials", headers={"WWW-Authenticate": "Basic"})

        encoded_credentials = auth_header[len("Basic "):].strip()
        logger.info(encoded_credentials)
        try:
            credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            logger.info(credentials)
            username, password = credentials.split(":", 1)
            logger.info(f"Authenticating username: {username} with provided password...")
            if await UsersController.validate_user(username, password):
                return AuthResult(user=username)
            else:
                raise NotAuthorized("Invalid user credentials", headers={"WWW-Authenticate": "Basic"})
        except (binascii.Error, ValueError):
            raise NotAuthorized("Invalid user credentials", headers={"WWW-Authenticate": "Basic"})
