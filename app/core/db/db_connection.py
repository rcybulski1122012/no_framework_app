import os

import psycopg2
import psycopg2.extras

from app.core.errors import MissingEnvironmentVariable

psycopg2.extras.register_uuid()


class DBConnection:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )

    def __del__(self):
        self.conn.close()

    def execute_query(self, query, data=None):
        with self.conn.cursor() as cur:
            cur.execute(query, data)
            try:
                result = cur.fetchall()
            except psycopg2.ProgrammingError:
                result = None
            self.conn.commit()

        return result


try:
    host = os.environ["DB_HOST"]
    database = os.environ["DB_NAME"]
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
except KeyError:
    raise MissingEnvironmentVariable("Please provide required environment variables")
else:
    db = DBConnection(host, database, user, password)
