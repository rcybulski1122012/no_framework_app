import app.models
from app.core.db.model import Model
from app.core.db.queries_generator import QueriesGenerator
from app.core.db.db_connection import db


models = []
for obj in app.models.__dict__.values():
    try:
        if issubclass(obj, Model) and obj != Model:
            models.append(obj)
    except TypeError:
        pass

for model in models:
    generator = QueriesGenerator(model)
    query = generator.get_create_table_query()
    db.execute_query(query)
