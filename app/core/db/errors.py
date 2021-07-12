class ModelException(Exception):
    pass


class MissingRequiredArgument(ModelException):
    pass


class ModelDoesNotExistInDb(ModelException):
    pass


class InvalidCondition(Exception):
    pass
