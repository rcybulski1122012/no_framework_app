import app.models
from app.core.db.db_connection import db
from app.core.db.model import Model
from app.core.db.queries_generator import QueriesGenerator as q
from app.core.http.sessions import Session


def create_tables(db_conn, models):
    for model in models:
        table_name = model.get_table_name()
        fields_repr = [q.get_field_sql_repr(field) for field in model._fields]
        query = q.get_create_table_query(table_name, fields_repr)
        db_conn.execute_query(query)


if __name__ == "__main__":
    models = [Session]
    for obj in app.models.__dict__.values():
        try:
            if issubclass(obj, Model) and obj != Model:
                models.append(obj)
        except TypeError:
            pass

    create_tables(db, models)
