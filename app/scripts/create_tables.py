from app.settings import models_modules
from app.core.db.model import Model
from app.core.http.sessions import Session


if __name__ == "__main__":
    models = [Session]
    for module in models_modules:
        for obj in module.__dict__.values():
            try:
                if issubclass(obj, Model) and obj != Model:
                    models.append(obj)
            except TypeError:
                pass

    for model in models:
        model.create_table()
