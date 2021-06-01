class Http400(Exception):
    pass


class Http404(Exception):
    pass


class MissingEnvironmentVariable(Exception):
    pass


class MissingRequiredArgument(Exception):
    pass


class ModelUpdateException(Exception):
    pass


class ModelDeletionException(Exception):
    pass
