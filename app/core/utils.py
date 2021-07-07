from app.core.db.model import Model


class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())


def get_models_from_modules(modules):
    models = []
    for module in modules:
        for obj in module.__dict__.values():
            try:
                if issubclass(obj, Model) and obj != Model:
                    models.append(obj)
            except TypeError:
                pass

    return models
