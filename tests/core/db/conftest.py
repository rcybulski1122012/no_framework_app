import pytest

from app.core.db.model import Field, Model
from app.core.db.queries_generator import QueriesGenerator


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


@pytest.fixture
def generator_model(model):
    return QueriesGenerator(model)


@pytest.fixture
def generator_instance(model):
    instance = model(first=1, second=2, third=3)
    return QueriesGenerator(instance)
