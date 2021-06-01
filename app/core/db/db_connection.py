import os
import psycopg2

from app.core.errors import MissingEnvironmentVariable


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

    def create_table_if_not_exists(self, model):
        query = model.get_create_table_query()

        with self.conn.cursor() as curs:
            curs.execute(query)
            self.conn.commit()


try:
    host = os.environ["HOST"]
    database = os.environ["DATABASE"]
    user = os.environ["USER"]
    password = os.environ["PASSWORD"]
except KeyError:
    raise MissingEnvironmentVariable("Please provide required environment variables")
else:
    db = DBConnection(host, database, user, password)

