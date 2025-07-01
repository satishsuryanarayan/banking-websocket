from sqlalchemy import Table, Column
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import Integer, DECIMAL, DateTime

from banking.apps.bank.v1.model.metadata import metadata

Transfers = Table(
    "transfers",
    metadata,
    Column("from_account_id", Integer, nullable=False, index=True),
    Column("to_account_id", Integer, nullable=False, index=True),
    Column("amount", DECIMAL(15, 2), nullable=False),
    Column("time", DateTime, default=func.now(), nullable=False, index=True),
)
