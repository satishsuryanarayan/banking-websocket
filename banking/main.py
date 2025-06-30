#!/usr/bin/env python
import os
import sys

from esmerald import Esmerald, Include, settings

from banking.apps.bank.v1.controller.utils.database import Database


def build_path():
    """
    Builds the path of the project and project root.
    """
    site_root = os.path.dirname(os.path.realpath(__file__))

    if site_root not in sys.path:
        sys.path.append(site_root)
        sys.path.append(os.path.join(site_root, "apps"))


async def startup():
    db_config = settings.db_config
    Database.connect(db_config)
    await Database.init()


async def shutdown():
    await Database.disconnect()


def get_application():
    build_path()

    app = Esmerald(
        routes=[Include(namespace="banking.urls")],
        on_startup=[startup],
        on_shutdown=[shutdown],
    )

    return app


app = get_application()
