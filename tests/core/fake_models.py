"""Used for testing app.core.utils.get_model_from_modules function """

from app.core.db.model import Model


class First(Model):
    pass


class Second(Model):
    pass


class Third(Model):
    pass


class NotAModel:
    pass


def function():
    pass
