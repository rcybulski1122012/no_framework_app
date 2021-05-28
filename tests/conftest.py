import pytest

from app.core.router import Router


@pytest.fixture
def router():
    return Router()


@pytest.fixture
def view(**kwargs):
    return lambda request: "Test view"
