import bcrypt

from app.auth.errors import UserDoesNotExist, InvalidPasswordError
from app.auth.models import AppUser


def authenticate(username, password):
    try:
        user = AppUser.select(username=username)[0]
    except IndexError:
        raise UserDoesNotExist("User with given username does not exist")

    hashed = user.password
    bin_passwd = bytes(password, "utf-8")

    if bcrypt.checkpw(bin_passwd, hashed):
        return user
    else:
        raise InvalidPasswordError("Given password does not match user password")
