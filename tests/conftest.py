import pytest

from app.router import Router


@pytest.fixture
def router():
    return Router()


@pytest.fixture
def view():
    return lambda request: "Test view"
