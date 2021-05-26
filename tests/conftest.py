import pytest

from app.core.router import Router


@pytest.fixture
def router():
    return Router()


@pytest.fixture
def view():
    return lambda request: "Test view"
