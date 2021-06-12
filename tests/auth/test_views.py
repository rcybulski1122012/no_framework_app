import pytest

from app.auth.models import AppUser
from app.auth.views import create_user_view
from app.core.errors import Http400
from tests.utils import json_request


@pytest.fixture(autouse=True)
def before_each(db_connection):
    AppUser.db = db_connection
    AppUser.create_table()


def test_create_user_view_creates_user_when_everything_is_ok():
    data = {"username": "username", "password1": "password", "password2": "password",
            "email": "emial@gmail.com"}
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert response.status_code == 201
    assert len(AppUser.select()) == 1


def test_create_user_view_raises_400_when_invalid_request_data():
    data = {"invalid": "data"}
    request = json_request("POST", "/register", data)

    with pytest.raises(Http400):
         create_user_view(request)


def test_create_user_view_returns_error_when_passwords_are_not_the_same():
    data = {"username": "username", "password1": "first", "password2": "second",
            "email": "email@gmail.com"}
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert "Both passwords should be the same." in response.body


def test_create_user_view_returns_error_when_username_is_taken():
    AppUser(username="taken_username", password="password", email="email@email.com").save()
    data = {"username": "taken_username", "password1": "password", "password2": "password",
            "email": "email@gmail.com"}
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert "This username is taken." in response.body


def test_create_user_view_returns_error_when_email_is_taken():
    AppUser(username="taken_username", password="password", email="email@gmail.com").save()
    data = {"username": "admin", "password1": "password", "password2": "password",
            "email": "email@gmail.com"}
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert "An account with this email already exists." in response.body

