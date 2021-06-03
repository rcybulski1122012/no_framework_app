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


class InstanceNotProvided(Exception):
    pass


class SessionDoesNotExist(Exception):
    pass
