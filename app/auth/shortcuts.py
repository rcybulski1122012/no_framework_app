import bcrypt

from app.auth.models import AppUser
from app.core.errors import ValidationError


def authenticate(username, password):
    try:
        user = AppUser.select(username=username)[0]
    except IndexError:
        raise ValidationError("User with given username does not exist.")

    hashed = user.password
    bin_passwd = bytes(password, "utf-8")

    if bcrypt.checkpw(bin_passwd, hashed):
        return user
    else:
        raise ValidationError("Given password does not match user password.")
