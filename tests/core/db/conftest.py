import pytest

from app.core.db.model import Field, Model


@pytest.fixture
def field():
    return Field("integer", nullable=False, default="5", unique=True, primary_key=True)


@pytest.fixture
def dummy_class():
    class Mock:
        pass

    return Mock


@pytest.fixture
def model():
    class TestModel(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    return TestModel
