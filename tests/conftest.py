import pytest

from app.core.router import Router


@pytest.fixture
def view(**kwargs):
    return lambda request: ("Test view", None)


@pytest.fixture
def router():
    return Router({})



