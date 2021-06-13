import pytest

from app.auth.models import AppUser
from app.auth.views import create_user_view, login_user_view
from app.core.errors import Http400
from app.core.http.sessions import Session
from app.scripts.install_extensions import install_extensions
from tests.utils import json_request


@pytest.fixture(autouse=True)
def before_each(db_connection):
    AppUser.db = db_connection
    AppUser.create_table()


@pytest.fixture
def SessionModel(db_connection):
    Session.db = db_connection
    install_extensions(db_connection, ["uuid-ossp"])
    Session.create_table()


def test_create_user_view_creates_user_when_everything_is_ok():
    data = {
        "username": "username",
        "password1": "password",
        "password2": "password",
        "email": "emial@gmail.com",
    }
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert response.status_code == 201
    assert len(AppUser.select()) == 1


def test_create_user_view_returns_405_when_invalid_method():
    request = json_request("GET", "/register", {})
    response = create_user_view(request)

    assert response.status_code == 405


def test_create_user_view_raises_400_when_invalid_request_data():
    data = {"invalid": "data"}
    request = json_request("POST", "/register", data)

    with pytest.raises(Http400):
        create_user_view(request)


def test_create_user_view_returns_error_when_passwords_are_not_the_same():
    data = {
        "username": "username",
        "password1": "first",
        "password2": "second",
        "email": "email@gmail.com",
    }
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert "Both passwords should be the same." in response.body


def test_create_user_view_returns_error_when_username_is_taken():
    AppUser(
        username="taken_username", password="password", email="email@email.com"
    ).save()
    data = {
        "username": "taken_username",
        "password1": "password",
        "password2": "password",
        "email": "email@gmail.com",
    }
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert "This username is taken." in response.body


def test_create_user_view_returns_error_when_email_is_taken():
    AppUser(
        username="taken_username", password="password", email="email@gmail.com"
    ).save()
    data = {
        "username": "admin",
        "password1": "password",
        "password2": "password",
        "email": "email@gmail.com",
    }
    request = json_request("POST", "/register", data)

    response = create_user_view(request)

    assert "An account with this email already exists." in response.body


def test_login_user_view_creates_session_object_and_creates_cookie(SessionModel):
    user = AppUser(username="username", password="password", email="email@gmail.com")
    user.save()
    data = {"username": "username", "password": "password"}
    request = json_request("POST", "/login", data)

    response = login_user_view(request)
    session = Session.select()[0]

    assert response.status_code == 201
    assert session["user_id"] == user.id_
    assert f"session_id={session.session_id}" in response.headers["Cookie"]


def test_login_user_view_returns_error_when_user_does_not_exist():
    data = {"username": "username", "password": "password"}
    request = json_request("POST", "/login", data)

    response = login_user_view(request)

    assert "User with this username does not exist." in response.body


def test_login_user_view_returns_error_when_invalid_password():
    AppUser(username="username", password="password", email="email@gmail.com").save()
    data = {"username": "username", "password": "invalid-password"}
    request = json_request("POST", "/login", data)

    response = login_user_view(request)

    assert "Invalid password." in response.body