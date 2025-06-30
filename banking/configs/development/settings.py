from typing import Optional

from esmerald.conf.enums import EnvironmentType

from ..settings import AppSettings


class DevelopmentAppSettings(AppSettings):
    debug: bool = True
    app_name: str = "Banking application in development mode."
    title: str = "Banking (Development)"
    environment: Optional[str] = EnvironmentType.DEVELOPMENT
