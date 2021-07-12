import pytest

from app.core.http.errors import Http404
from app.core.http.request import HttpRequest
from app.core.http.sessions import Session
from app.views import index, static


def test_index_renders_authentication_html_when_user_is_not_logged_in():
    raw_request = f"GET / HTTP/1.1\n\n"
    request = HttpRequest(bytes(raw_request, "utf-8"))
    response = index(request)

    assert "login-form" in response.body


def test_index_renders_index_html_when_user_is_logged_in():
    session = Session.create(data='{"user_id": 1}')
    raw_request = (
        f"GET /users/1/todolists HTTP/1.1\nCookie: session_id={session.session_id}\n\n"
    )
    request = HttpRequest(bytes(raw_request, "utf-8"))
    response = index(request)

    assert "login-form" not in response.body


def test_static_raises_404_when_invalid_filename_format():
    with pytest.raises(Http404):
        static(None, "invalid-file-name")


def test_static_raises_404_when_invalid_file_type():
    with pytest.raises(Http404):
        static(None, "invalid_mime_type.py")
