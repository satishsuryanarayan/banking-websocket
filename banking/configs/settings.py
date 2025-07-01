from functools import cached_property
from typing import Optional, Literal

from esmerald.conf.enums import EnvironmentType
from esmerald.conf.global_settings import EsmeraldAPISettings

IsolationLevel = Literal["REPEATABLE READ", "SERIALIZABLE"]


class AppSettings(EsmeraldAPISettings):
    app_name: str = "Banking application in production mode."
    title: str = "Banking (Production)"
    environment: Optional[str] = EnvironmentType.PRODUCTION
    secret_key: str = "esmerald-insecure-8#^lz#h&amp;l647#y2s33djuw3ygfi@&amp;8k258-(%d#ssy5&amp;b3&amp;fj%"
    debug: bool = True

    @property
    def initdb(self) -> bool:
        return True

    @property
    def serializable(self) -> IsolationLevel:
        return "SERIALIZABLE"

    @property
    def repeatable_read(self) -> IsolationLevel:
        return "REPEATABLE READ"

    @property
    def pool_size(self):
        return 2

    @property
    def mysql_username(self) -> str:
        return "banker"

    @property
    def mysql_password(self) -> str:
        return "secret"

    @property
    def mysql_host(self) -> str:
        return "mysql-container"

    @property
    def mysql_database(self) -> str:
        return "bank"

    @cached_property
    def sql_alchemy_url(self) -> str:
        url = "mysql+aiomysql://{0}:{1}@{2}/{3}".format(self.mysql_username, self.mysql_password, self.mysql_host,
                                                       self.mysql_database)
        return url

    @cached_property
    def db_config(self) -> dict:
        config = dict()
        config["url"] = self.sql_alchemy_url
        config["isolation_level"] = self.serializable
        config["pool_size"] = self.pool_size
        config["pool_pre_ping"] = True
        config["pool_timeout"] = 30
        config["max_overflow"] = 0
        config["pool_reset_on_return"] = "rollback"

        return config
