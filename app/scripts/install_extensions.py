from app.core.db.db_connection import db
from app.settings import psql_extensions


def install_extensions(db_conn, extensions):
    for extension in extensions:
        query = f'CREATE EXTENSION IF NOT EXISTS "{extension}";'
        db_conn.execute_query(query)


if __name__ == "__main__":
    install_extensions(db, psql_extensions)
