from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Table, Column
from sqlalchemy.sql.sqltypes import Integer, DECIMAL, DateTime

from banking.apps.bank.v1.model.metadata import metadata

Balances = Table(
    "balances",
    metadata,
    Column("account_id", Integer, nullable=False, index=True),
    Column("amount", DECIMAL(15, 2), nullable=False),
    Column("last_updated_time", DateTime, default=func.now(), onupdate=func.now(), nullable=False)
)
