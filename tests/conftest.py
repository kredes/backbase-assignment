from typing import Iterator

import pytest
from starlette.testclient import TestClient

from api.app import app


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    yield TestClient(app)
