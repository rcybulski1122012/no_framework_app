import json

from app.core.db.model import Model
from app.core.errors import Http400


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


def get_data_from_request_body(request, fields_names):
    try:
        data = json.loads(request.body)
        result = [data[field_name] for field_name in fields_names]
    except (json.decoder.JSONDecodeError, KeyError):
        raise Http400
    else:
        return result
