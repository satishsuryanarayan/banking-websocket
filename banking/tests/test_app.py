import pytest
from esmerald.testclient import EsmeraldTestClient

from ..main import get_application

pytestmark = pytest.mark.anyio

basr_url = "http://127.0.0.1:8000/v1/"

def create_app():
    app = get_application()
    return app


def get_client():
    return EsmeraldTestClient(create_app())


@pytest.fixture(scope="session")
def client():
    return get_client()
