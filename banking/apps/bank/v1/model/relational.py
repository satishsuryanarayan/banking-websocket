from sqlalchemy import DDL, event
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.schema import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, DECIMAL, LargeBinary, String

metadata: MetaData = MetaData()

Users = Table(
    "users",
    metadata,
    Column("username", String(20), primary_key=True, nullable=False, index=True),
    Column("password", LargeBinary, nullable=False),
    Column("email", String(120), nullable=False)
)

Customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("name", String(50), nullable=False),
    Column("creation_time", DateTime, default=func.now(), nullable=False, index=True)
)

Accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=False, index=True),
    Column("creation_time", DateTime, default=func.now(), nullable=False, index=True)
)

Balances = Table(
    "balances",
    metadata,
    Column("account_id", Integer, nullable=False, index=True),
    Column("amount", DECIMAL(15, 2), nullable=False),
    Column("last_updated_time", DateTime, default=func.now(), onupdate=func.now(), nullable=False)
)

Transfers = Table(
    "transfers",
    metadata,
    Column("from_account_id", Integer, nullable=False, index=True),
    Column("to_account_id", Integer, nullable=False, index=True),
    Column("amount", DECIMAL(15, 2), nullable=False),
    Column("time", DateTime, default=func.now(), nullable=False, index=True),
)

event.listen(
    Balances,
    "after_create",
    DDL(
        "ALTER TABLE balances PARTITION BY HASH(account_id) PARTITIONS 1000;"
    ),
)

event.listen(
    Transfers,
    "after_create",
    DDL(
        """
            ALTER TABLE transfers PARTITION BY RANGE (YEAR(time))
                SUBPARTITION BY KEY(MONTH(time))
                SUBPARTITIONS 12 (
                    PARTITION p0 VALUES LESS THAN (2026) ENGINE = InnoDB,
                    PARTITION p1 VALUES LESS THAN (2027) ENGINE = InnoDB,
                    PARTITION p2 VALUES LESS THAN (2028) ENGINE = InnoDB,
                    PARTITION p3 VALUES LESS THAN (2029) ENGINE = InnoDB,
                    PARTITION p4 VALUES LESS THAN (2030) ENGINE = InnoDB,
                    PARTITION p5 VALUES LESS THAN (2031) ENGINE = InnoDB,
                    PARTITION p6 VALUES LESS THAN (2032) ENGINE = InnoDB,
                    PARTITION p7 VALUES LESS THAN (2033) ENGINE = InnoDB,
                    PARTITION p8 VALUES LESS THAN (2034) ENGINE = InnoDB,
                    PARTITION p9 VALUES LESS THAN (2035) ENGINE = InnoDB,
                    PARTITION p10 VALUES LESS THAN (2036) ENGINE = InnoDB,
                    PARTITION p11 VALUES LESS THAN (2037) ENGINE = InnoDB,
                    PARTITION p12 VALUES LESS THAN (2038) ENGINE = InnoDB,
                    PARTITION p13 VALUES LESS THAN (2039) ENGINE = InnoDB,
                    PARTITION p14 VALUES LESS THAN (2040) ENGINE = InnoDB,
                    PARTITION p15 VALUES LESS THAN (2041) ENGINE = InnoDB,
                    PARTITION p16 VALUES LESS THAN (2042) ENGINE = InnoDB,
                    PARTITION p17 VALUES LESS THAN (2043) ENGINE = InnoDB,
                    PARTITION p18 VALUES LESS THAN (2044) ENGINE = InnoDB,
                    PARTITION p19 VALUES LESS THAN (2045) ENGINE = InnoDB,
                    PARTITION p20 VALUES LESS THAN (2046) ENGINE = InnoDB,
                    PARTITION p21 VALUES LESS THAN (2047) ENGINE = InnoDB,
                    PARTITION p22 VALUES LESS THAN (2048) ENGINE = InnoDB,
                    PARTITION p23 VALUES LESS THAN (2049) ENGINE = InnoDB,
                    PARTITION p24 VALUES LESS THAN (2050) ENGINE = InnoDB,
                    PARTITION p25 VALUES LESS THAN MAXVALUE ENGINE = InnoDB
                );
        """
    ),
)
