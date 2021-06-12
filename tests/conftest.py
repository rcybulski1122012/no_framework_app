import psycopg2
import pytest


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
