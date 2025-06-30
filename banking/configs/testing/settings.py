from typing import Optional

from esmerald.conf.enums import EnvironmentType

from ..settings import AppSettings


class TestingAppSettings(AppSettings):
    debug: bool = True
    app_name: str = "Banking application in testing mode."
    title: str = "Banking (Testing)"
    environment: Optional[str] = EnvironmentType.TESTING
    secret_key: str = ""

    @property
    def pool_size(self):
        return 2

    @property
    def mysql_database(self) -> str:
        return "test_bank"
