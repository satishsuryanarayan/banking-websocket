from datetime import datetime
from decimal import Decimal
from typing import cast, AsyncGenerator

from esmerald.logging import logger
from sqlalchemy import insert, select, update, and_, or_
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import TimeoutError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncResult
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import exists

from banking.apps.bank.v1.controller.utils.database import Database
from banking.apps.bank.v1.controller.utils.listgenerator import list_generator
from banking.apps.bank.v1.model.relational import Accounts
from banking.apps.bank.v1.model.relational import Balances
from banking.apps.bank.v1.model.relational import Transfers


class TransfersController:
    @classmethod
    async def create_transfer(cls, from_account_id: int, to_account_id: int, amount: Decimal) -> Transfers:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="SERIALIZABLE")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(select(exists().where(
                    cast(ColumnElement[bool], Accounts.c.id == from_account_id))))
                from_exists: int = cursor.scalar()
                if not from_exists:
                    raise AssertionError(f"Account with id={from_account_id} does not exist")

                cursor: CursorResult = await connection.execute(select(
                    exists().where(cast(ColumnElement[bool], Accounts.c.id == to_account_id))))
                to_exists: int = cursor.scalar()
                if not to_exists:
                    raise AssertionError(f"Account with id={to_account_id} does not exist")

                """
                Consistent ordering of operations reduces the likelihood of deadlocks
                and, to that effect, whether transferring money from account 1 to account 2 or
                from account 2 to account 1, the database locks are acquired in the same order
                i.e. first lock for account 1 is acquired and then lock for account 2 is acquired.
                """
                if from_account_id < to_account_id:
                    cursor: CursorResult = await connection.execute(select(Balances.c.amount).where(
                        cast(ColumnElement[bool],
                             Balances.c.account_id == from_account_id)).with_for_update())
                    from_account_balance: Decimal = cursor.scalar()
                    if from_account_balance < amount:
                        raise AssertionError(
                            f"Balance in account with id={from_account_id} is {from_account_balance} which is not enough to transfer {amount}")

                    cursor: CursorResult = await connection.execute(select(Balances.c.amount).where(
                        cast(ColumnElement[bool],
                             Balances.c.account_id == to_account_id)).with_for_update())
                    to_account_balance: Decimal = cursor.scalar()
                else:
                    cursor: CursorResult = await connection.execute(select(Balances.c.amount).where(
                        cast(ColumnElement[bool],
                             Balances.c.account_id == to_account_id)).with_for_update())
                    to_account_balance: Decimal = cursor.scalar()

                    cursor: CursorResult = await connection.execute(select(Balances.c.amount).where(
                        cast(ColumnElement[bool],
                             Balances.c.account_id == from_account_id)).with_for_update())
                    from_account_balance: Decimal = cursor.scalar()
                    if from_account_balance < amount:
                        raise AssertionError(
                            f"Balance in account with id={from_account_id} is {from_account_balance} which is not enough to transfer {amount}")

                from_account_balance = from_account_balance - amount
                to_account_balance = to_account_balance + amount
                now: datetime = datetime.now()

                await connection.execute(update(Balances).where(
                    cast(ColumnElement[bool], Balances.c.account_id == from_account_id)).values(
                    amount=from_account_balance, last_updated_time=now))
                await connection.execute(update(Balances).where(
                    cast(ColumnElement[bool], Balances.c.account_id == to_account_id)).values(
                    amount=to_account_balance, last_updated_time=now))
                await connection.execute(
                    insert(Transfers).values(from_account_id=from_account_id,
                                             to_account_id=to_account_id, amount=amount,
                                             time=now))
                transfer: Transfers = Transfers(from_account_id=from_account_id,
                                                to_account_id=to_account_id,
                                                amount=amount, time=now)
                return transfer
        except AssertionError as ae:
            logger.info("Forbidden: %s", ae, exc_info=True)
            raise ae
        except Exception as e:
            logger.error("Unknown error while transferring money: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()

    @classmethod
    async def get_account_transfers(cls, account_id: int, from_time: datetime,
                                    to_time: datetime) -> AsyncGenerator[str]:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            cursor: CursorResult = await connection.execute(
                select(exists().where(cast(ColumnElement[bool], Accounts.c.id == account_id))))
            account_exists: int = cursor.scalar()
            if not account_exists:
                raise AssertionError(f"Account with id={account_id} does not exist")
            cursor: AsyncResult = await connection.stream(
                select(Transfers).where(and_(Transfers.c.time.between(from_time, to_time),
                                             or_(Transfers.c.from_account_id == account_id,
                                                 Transfers.c.to_account_id == account_id))).order_by(Transfers.c.time))
            return list_generator(cursor.mappings(), connection, Transfers)
        except AssertionError as ae:
            await connection.rollback()
            await connection.close()
            logger.info("Forbidden: %s", ae, exc_info=True)
            raise ae
        except Exception as e:
            await connection.rollback()
            await connection.close()
            logger.error("Unknown error while getting transfers for a given account: %s", e, exc_info=True)
            raise e
