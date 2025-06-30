from sqlalchemy import Table, Column, event, DDL
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

event.listen(
    Transfers,
    "after_create",
    DDL(
        """
            ALTER TABLE transfers PARTITION BY RANGE (YEAR(time))
                SUBPARTITION BY HASH (MONTH(time))
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