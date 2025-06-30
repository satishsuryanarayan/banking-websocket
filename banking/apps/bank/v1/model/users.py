from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, LargeBinary

from banking.apps.bank.v1.model.metadata import metadata

Users = Table(
    "users",
    metadata,
    Column("username", String(20), primary_key=True, nullable=False, index=True),
    Column("password", LargeBinary, nullable=False),
    Column("email", String(120), nullable=False)
)
