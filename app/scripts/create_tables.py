import app.models
from app.core.db import Model, QueriesGenerator, db
from app.core.http import Session

models = [Session]
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
