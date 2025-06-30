from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime

from banking.apps.bank.v1.model.metadata import metadata

Accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=False, index=True),
    Column("creation_time", DateTime, default=func.now(), nullable=False, index=True)
)
