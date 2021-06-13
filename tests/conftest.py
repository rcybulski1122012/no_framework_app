import psycopg2
import pytest

from app.core.utils import get_models_from_modules
from app.scripts.install_extensions import install_extensions
from app.settings import models_modules, psql_extensions


def pytest_configure(config):
    config.addinivalue_line("markers", "disable_before_each_fixture")


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


@pytest.fixture(autouse=True)
def before_each(request, db_connection):
    if "disable_before_each_fixture" in request.keywords:
        return

    install_extensions(db_connection, psql_extensions)
    models = get_models_from_modules(models_modules)

    for model in models:
        model.db = db_connection
        model.create_table()
