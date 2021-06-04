import app.models
from app.core.db.model import Model
from app.core.http.sessions import Session
from app.core.db.queries import get_create_table_query, get_field_sql_repr

models = [Session]
for obj in app.models.__dict__.values():
    try:
        if issubclass(obj, Model) and obj != Model:
            models.append(obj)
    except TypeError:
        pass

for model in models:
    table_name = model.get_table_name()
    fields_repr = [get_field_sql_repr(field) for field in model._fields]
    query = get_create_table_query(table_name, fields_repr)
    model._db.execute_query(query)
