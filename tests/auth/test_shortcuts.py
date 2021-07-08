import pytest

from app.auth.models import AppUser
from app.auth.shortcuts import authenticate
from app.core.errors import ValidationError


def test_authenticate_returns_user_when_everything_is_ok():
    username, password = "Username", "Password0!"
    user = AppUser.create(username=username, password=password, email="email@gmail.com")

    result = authenticate(username, password)

    assert str(result) == str(user)


def test_authenticate_raises_exception_when_wrong_username():
    with pytest.raises(ValidationError):
        authenticate("username", "password")


def test_authenticate_raises_exception_when_passwords_do_not_match():
    username, password = "Username", "Password0!"
    AppUser.create(username=username, password=password, email="email@gmail.com")

    with pytest.raises(ValidationError):
        authenticate(username, "wrong-password")
