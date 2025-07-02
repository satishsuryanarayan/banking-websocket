from typing import cast

import bcrypt
from bank.datamodel.v1.dtos.user import UserDTO
from esmerald.logging import logger
from sqlalchemy import insert, select, CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import exists

from banking.apps.bank.v1.controller.utils.database import Database
from banking.apps.bank.v1.model.relational import Users


class UsersController:
    @classmethod
    async def register_user(cls, username: str, password: str, email: str) -> UserDTO:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="SERIALIZABLE")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(
                    select(
                        exists().where(cast(ColumnElement[bool], Users.c.username == username))))
                user_exists: int = cursor.scalar()
                if not user_exists:
                    hashed_password: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=6))
                    await connection.execute(
                        insert(Users).values(username=username, password=hashed_password,
                                             email=email))
                    user: UserDTO = UserDTO(username=username, password=hashed_password.decode(),
                                            email=email)
                    return user
                else:
                    raise AssertionError(f"Username={username} already exists")
        except AssertionError as ae:
            logger.error("Assertion failure: %s", ae, exc_info=False)
            raise ae
        except Exception as e:
            logger.error("Unknown error while adding user: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()

    @classmethod
    async def validate_user(cls, username: str, password: str) -> bool:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(
                    select(exists().where(cast(ColumnElement[bool], Users.c.username == username))))
                user_exists: int = cursor.scalar()
                if user_exists:
                    cursor: CursorResult = await connection.execute(
                        select(Users.c.password).where(
                            cast(ColumnElement[bool], Users.c.username == username)))
                    pwd: bytes = cursor.scalar()
                    if bcrypt.checkpw(password.encode(), pwd):
                        return True
                    else:
                        raise AssertionError(f"Password invalid for username={username}")
                else:
                    raise AssertionError(f"Username={username} does not exist")
        except AssertionError as ae:
            logger.error("Assertion failure: %s", ae, exc_info=False)
            return False
        except Exception as e:
            logger.error("Unknown error while validating user: %s", e, exc_info=True)
            return False
        finally:
            await connection.close()
