class AuthenticationError(Exception):
    pass


class UserDoesNotExist(AuthenticationError):
    pass


class PasswordsDoNotMatch(AuthenticationError):
    pass
