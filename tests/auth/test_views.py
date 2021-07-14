import json

import pytest

from app.auth.models import AppUser
from app.auth.views import create_user_view, login_user_view, logout_view
from app.core.http.errors import Http400, Http403, Http405
from app.core.http.sessions import Session
from tests.utils import create_request


def test_create_user_view_creates_user_when_everything_is_ok():
    data = {
        "username": "username",
        "password1": "Password0!",
        "password2": "Password0!",
        "email": "emial@gmail.com",
    }
    request = create_request("POST", "/register", "HTTP/1.1", body=data)

    response = create_user_view(request)

    assert response.status_code == 201
    assert len(AppUser.select()) == 1


def test_create_user_view_raises_405_when_invalid_method():
    request = create_request("GET", "/register", "HTTP/1.1", body={})

    with pytest.raises(Http405):
        create_user_view(request)


def test_create_user_view_raises_400_when_invalid_request_data():
    data = {"invalid": "data"}
    request = create_request("POST", "/register", "HTTP/1.1", body=data)

    with pytest.raises(Http400):
        create_user_view(request)


def test_create_user_view_returns_error_when_passwords_are_not_the_same():
    data = {
        "username": "username",
        "password1": "Password1!",
        "password2": "Password2!",
        "email": "email@gmail.com",
    }
    request = create_request("POST", "/register", "HTTP/1.1", body=data)

    response = create_user_view(request)

    assert "Both passwords should be the same." in response.body


def test_create_user_view_returns_error_when_username_is_taken():
    AppUser.create(
        username="taken_username", password="Password0!", email="email@email.com"
    )
    data = {
        "username": "taken_username",
        "password1": "Password0!",
        "password2": "Password0!",
        "email": "email@gmail.com",
    }
    request = create_request("POST", "/register", "HTTP/1.1", body=data)

    response = create_user_view(request)

    assert "This username is taken." in response.body


def test_create_user_view_returns_error_when_email_is_taken():
    AppUser.create(
        username="taken_username", password="Password0!", email="email@gmail.com"
    )
    data = {
        "username": "username",
        "password1": "Password0!",
        "password2": "Password0!",
        "email": "email@gmail.com",
    }
    request = create_request("POST", "/register", "HTTP/1.1", body=data)

    response = create_user_view(request)

    assert "An account with this email already exists." in response.body


def test_login_user_view_creates_session_object_and_creates_cookie():
    user = AppUser.create(
        username="username", password="Password0!", email="email@gmail.com"
    )
    data = {"username": "username", "password": "Password0!"}
    request = create_request("POST", "/login", "HTTP/1.1", body=data)

    response = login_user_view(request)
    body = json.loads(response.body)
    session = Session.select()[0]

    assert response.status_code == 201
    assert session["user_id"] == user.id_
    assert body["session_id"] == str(session.session_id)


def test_login_user_view_returns_error_when_user_does_not_exist():
    data = {"username": "username", "password": "Password0!"}
    request = create_request("POST", "/login", "HTTP/1.1", body=data)

    response = login_user_view(request)

    assert "User with given username does not exist." in response.body


def test_login_user_view_returns_error_when_invalid_password():
    AppUser.create(username="username", password="Password0!", email="email@gmail.com")
    data = {"username": "username", "password": "invalid-password"}
    request = create_request("POST", "/login", "HTTP/1.1", body=data)

    response = login_user_view(request)

    assert "Given password does not match user password." in response.body


def test_login_user_view_raises_405_when_invalid_method():
    request = create_request("GET", "/login", "HTTP/1.1", body={})

    with pytest.raises(Http405):
        login_user_view(request)


def test_logout_view_deletes_the_session_and_redirects(user_and_session):
    user, session = user_and_session
    request = create_request("POST", "/logout", "HTTP/1.1", session=session)
    response = logout_view(request)

    result = Session.select(id_=session.id_)

    assert result == []
    assert response.status_code == 302


def test_logout_view_raises_403_when_not_logged_in():
    request = create_request("POST", "/logout", "HTTP/1.1")

    with pytest.raises(Http403):
        logout_view(request)
