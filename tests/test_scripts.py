from app.scripts.drop_tables import delete_tables
from app.scripts.install_extensions import install_extensions
from tests.core.db.utils import get_all_tables


def test_install_extensions(db_connection):
    extensions = ["hstore", "uuid-ossp"]
    install_extensions(db_connection, extensions)
    result = [
        row[0]
        for row in db_connection.execute_query("SELECT extname FROM pg_extension;")
    ]

    assert "hstore" in result
    assert "uuid-ossp" in result


def test_drop_tables(db_connection):
    db_connection.execute_query("CREATE TABLE test_table (id_ serial PRIMARY KEY);")
    delete_tables(db_connection)
    assert get_all_tables(db_connection) == []
