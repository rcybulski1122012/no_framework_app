import pytest

from app.auth.errors import PasswordsDoNotMatch, UserDoesNotExist
from app.auth.models import AppUser
from app.auth.shortcuts import authenticate


def test_authenticate_returns_user_when_everything_is_ok():
    username, password = "username", "password"
    user = AppUser(username=username, password=password, email="email")
    user.save()

    result = authenticate(username, password)

    assert str(result) == str(user)


def test_authenticate_raises_exception_when_wrong_username():
    with pytest.raises(UserDoesNotExist):
        authenticate("username", "password")


def test_authenticate_raises_exception_when_passwords_do_not_match():
    username, password = "username", "password"
    user = AppUser(username=username, password=password, email="email")
    user.save()

    with pytest.raises(PasswordsDoNotMatch):
        authenticate(username, "wrong-password")
