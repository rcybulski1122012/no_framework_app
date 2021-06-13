from app.core.utils import get_models_from_modules
from app.settings import models_modules

if __name__ == "__main__":
    models = get_models_from_modules(models_modules)

    for model in models:
        model.create_table()
