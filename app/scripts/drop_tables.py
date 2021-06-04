from app.core.db.db_connection import db


def delete_tables(db_conn):
    query = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    db_conn.execute_query(query)


if __name__ == "__main__":
    delete_tables(db)
