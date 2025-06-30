from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

from banking.apps.bank.v1.model.metadata import metadata

Customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("name", String(50), nullable=False),
    Column("creation_time", DateTime, default=func.now(), nullable=False, index=True)
)
