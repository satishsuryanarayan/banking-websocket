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
from banking.apps.bank.v1.dtos.account import Account
from banking.apps.bank.v1.dtos.balance import Balance
from banking.apps.bank.v1.dtos.createaccount import CreateAccount
from banking.apps.bank.v1.model.accounts import Accounts
from banking.apps.bank.v1.model.balances import Balances
from banking.apps.bank.v1.model.customers import Customers


class AccountsController:
    @classmethod
    async def get_all_accounts(cls, from_time: datetime = None, to_time: datetime = None) -> AsyncGenerator[str]:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            if from_time is not None and to_time is not None:
                cursor: AsyncResult = await connection.stream(
                    select(Accounts).where(
                        and_(Accounts.c.creation_time >= from_time, Accounts.c.creation_time <= to_time)).order_by(
                        Accounts.c.creation_time))
            elif from_time is not None and to_time is None:
                cursor: AsyncResult = await connection.stream(
                    select(Accounts).where(Accounts.c.creation_time >= from_time).order_by(Accounts.c.creation_time))
            elif from_time is None and to_time is not None:
                cursor: AsyncResult = await connection.stream(
                    select(Accounts).where(Accounts.c.creation_time <= to_time).order_by(Accounts.c.creation_time))
            else:
                cursor: AsyncResult = await connection.stream(
                    select(Accounts).order_by(Accounts.c.creation_time))

            return list_generator(cursor.mappings(), connection, Account)
        except Exception as e:
            await connection.rollback()
            await connection.close()
            logger.error("Unknown error while getting all accounts: %s", e, exc_info=True)
            raise e

    @classmethod
    async def create_account(cls, crt_account: CreateAccount) -> Account:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="SERIALIZABLE")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(select(
                    exists().where(cast(ColumnElement[bool], Customers.c.id == crt_account.customer_id))))
                customer_exists: int = cursor.scalar()
                if not customer_exists:
                    raise AssertionError(f"Customer with id={crt_account.customer_id} does not exist")

                now: datetime = datetime.now()
                cursor: CursorResult = await connection.execute(
                    insert(Accounts).values(customer_id=crt_account.customer_id, creation_time=now))
                account_id: int = cursor.inserted_primary_key[0]
                cursor.close()
                await connection.execute(
                    insert(Balances).values(account_id=account_id, amount=crt_account.amount,
                                            last_updated_time=now))
                account: Account = Account(id=account_id, customer_id=crt_account.customer_id, creation_time=now)
                return account
        except AssertionError as ae:
            logger.info("Forbidden: %s", ae, exc_info=True)
            raise ae
        except Exception as e:
            logger.error("Unknown error while creating account: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()

    @classmethod
    async def get_account(cls, account_id: int) -> Account:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(
                    select(exists().where(cast(ColumnElement[bool], Accounts.c.id == account_id))))
                account_exists: int = cursor.scalar()
                if not account_exists:
                    raise AssertionError(f"Account with id={account_id} does not exist")
                cursor: CursorResult = await connection.execute(
                    select(Accounts).where(cast(ColumnElement[bool], Accounts.c.id == account_id)))
                account: Account = Account.model_validate(cursor.mappings().first())
                cursor.close()
                return account
        except AssertionError as ae:
            logger.info("Forbidden: %s", ae, exc_info=True)
            raise ae
        except Exception as e:
            logger.error("Unknown error while getting account: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()

    @classmethod
    async def get_customer_accounts(cls, customer_id: int) -> AsyncGenerator[str]:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            cursor: CursorResult = await connection.execute(
                select(exists().where(cast(ColumnElement[bool], Customers.c.id == customer_id))))
            customer_exists: int = cursor.scalar()
            if not customer_exists:
                raise AssertionError(f"Customer with id={customer_id} does not exist")
            cursor: AsyncResult = await connection.stream(
                select(Accounts).where(cast(ColumnElement[bool], Accounts.c.customer_id == customer_id)).order_by(
                    Accounts.c.id))

            return list_generator(cursor.mappings(), connection, Account)
        except AssertionError as ae:
            await connection.rollback()
            await connection.close()
            logger.info("Forbidden: %s", ae, exc_info=True)
            raise ae
        except Exception as e:
            await connection.rollback()
            await connection.close()
            logger.error("Unknown error while getting customer accounts: %s", e, exc_info=True)
            raise e

    @classmethod
    async def get_account_balance(cls, account_id: int) -> Balance:
        try:
            connection: AsyncConnection = await Database.get_connection(isolation_level="REPEATABLE READ")
        except TimeoutError as pe:
            logger.warning("Not enough resources: %s", pe, exc_info=True)
            raise ResourceWarning(pe)

        try:
            async with connection.begin():
                cursor: CursorResult = await connection.execute(
                    select(exists().where(cast(ColumnElement[bool], Accounts.c.id == account_id))))
                account_exists: int = cursor.scalar()
                if not account_exists:
                    raise AssertionError(f"Account with id={account_id} does not exist")
                cursor: CursorResult = await connection.execute(
                    select(Balances).where(cast(ColumnElement[bool], Balances.c.account_id == account_id)))
                balance: Balance = Balance.model_validate(cursor.mappings().first())
                cursor.close()

                return balance
        except AssertionError as ae:
            logger.info("Forbidden: %s", ae, exc_info=True)
            raise ae
        except Exception as e:
            logger.error("Unknown error while getting account balance: %s", e, exc_info=True)
            raise e
        finally:
            await connection.close()
