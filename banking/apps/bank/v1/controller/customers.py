from datetime import datetime
from typing import cast, AsyncGenerator

from esmerald.logging import logger
from sqlalchemy import insert, select, and_
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import TimeoutError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncResult
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import exists

from banking.apps.bank.v1.controller.utils.database import Database
from banking.apps.bank.v1.controller.utils.listgenerator import list_generator
from banking.apps.bank.v1.model.relational import Customers


class CustomersController:
    @classmethod
    async def get_all_customers(cls, from_time: datetime = None, to_time: datetime = None) -> AsyncGenerator[str]:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            if from_time is not None and to_time is not None:
                cursor: AsyncResult = await connection.stream(
                    select(Customers).where(
                        and_(Customers.c.creation_time >= from_time, Customers.c.creation_time <= to_time)).order_by(
                        Customers.c.creation_time))
            elif from_time is not None and to_time is None:
                cursor: AsyncResult = await connection.stream(
                    select(Customers).where(Customers.c.creation_time >= from_time).order_by(Customers.c.creation_time))
            elif from_time is None and to_time is not None:
                cursor: AsyncResult = await connection.stream(
                    select(Customers).where(Customers.c.creation_time <= to_time).order_by(Customers.c.creation_time))
            else:
                cursor: AsyncResult = await connection.stream(
                    select(Customers).order_by(Customers.c.creation_time))

            return list_generator(cursor.mappings(), connection, Customers)
        except Exception as e:
            await connection.rollback()
            await connection.close()
            logger.error("Unknown error while creating customer: %s", e, exc_info=True)
            raise e

    @classmethod
    async def create_customer(cls, name: str) -> Customers:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="SERIALIZABLE")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                now: datetime = datetime.now()
                cursor: CursorResult = await connection.execute(
                    insert(Customers).values(name=name, creation_time=now))
                customer_id: int = cursor.inserted_primary_key[0]
                cursor.close()
                customer: Customers = Customers(id=customer_id, name=name, creation_time=now)
                return customer
        except Exception as e:
            logger.error("Unknown error while creating customer: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()

    @classmethod
    async def get_customer(cls, customer_id: int) -> Customers:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(
                    select(exists().where(cast(ColumnElement[bool], Customers.c.id == customer_id))))
                customer_exists: int = cursor.scalar()
                if not customer_exists:
                    raise AssertionError(f"Customer with id={customer_id} does not exist")
                cursor: CursorResult = await connection.execute(
                    select(Customers).where(cast(ColumnElement[bool], Customers.c.id == customer_id)))
                customer: Customers = Customers.model_validate(cursor.mappings().first())
                cursor.close()
                return customer
        except Exception as e:
            logger.error("Unknown error while getting customer: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()
