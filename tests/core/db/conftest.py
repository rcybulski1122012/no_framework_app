import psycopg2
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
def db_connection(postgresql):
    class PostgresDBConnection:
        conn = postgresql

        def execute_query(self, query, data=None):
            with self.conn.cursor() as cur:
                cur.execute(query, data)
                try:
                    result = cur.fetchall()
                except psycopg2.ProgrammingError:
                    result = None
                self.conn.commit()

            return result

    return PostgresDBConnection()


@pytest.fixture
def model(db_connection):
    class TestModel(Model):
        db = db_connection

        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    return TestModel


@pytest.fixture
def instance(model):
    return model(first=1, second=2, third=3)
