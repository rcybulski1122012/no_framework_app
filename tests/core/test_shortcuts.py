from pathlib import Path
import uuid

import pytest

from app.core.errors import SessionDoesNotExist
from app.scripts.install_extensions import install_extensions
from app.core.http.request import HttpRequest
from app.core.http.sessions import Session
from app.core.shortcuts import json_response, render_template, get_current_session


def test_render_template(tmpdir, GET_request_obj):
    p = tmpdir.mkdir("files").join("file.html")
    p.write("content")
    response_body = render_template(
        GET_request_obj, "file.html", templates_dir=Path(p.dirpath())
    ).body
    assert response_body == "content"


@pytest.mark.parametrize(
    "variable_format",
    [
        "{{var}}",
        "{{ var }}",
        "{{var }}",
        "{{ var}}",
        "{{      var       }}",
        "{{\t\t \t \n var \t }}",
    ],
)
def test_render_template_replaces_variables(tmpdir, variable_format, GET_request_obj):
    p = tmpdir.mkdir("files").join("file.html")
    p.write(f"content {variable_format}")

    response_body = render_template(
        GET_request_obj, "file.html", templates_dir=Path(p.dirpath()), var="Variable"
    ).body
    assert response_body == "content Variable"


def test_json_response(GET_request_obj):
    expected = '{"test": 2, "values": ["t", "e", "s", "t"]}'
    response_body = json_response(
        GET_request_obj, {"test": 2, "values": ["t", "e", "s", "t"]}
    ).body

    assert response_body == expected


def test_get_current_session_returns_session(db_connection):
    Session.db = db_connection
    install_extensions(db_connection, ["uuid-ossp"])
    Session.create_table()
    session = Session(data='{"user_id": 1}')
    session.save()
    session = Session.select()[0]
    raw_request = bytes(f"GET / HTTP/1.1\nCookie: session_id={session.session_id}\n", "utf-8")
    request = HttpRequest(raw_request)
    result = get_current_session(request)

    assert str(result) == str(session)


def test_get_current_session_raises_exception_when_session_id_not_in_cookie():
    raw_request = bytes(f"GET / HTTP/1.1\n", "utf-8")
    request = HttpRequest(raw_request)

    with pytest.raises(SessionDoesNotExist):
        get_current_session(request)


def test_get_current_session_raises_exception_when_session_not_id_db(db_connection):
    Session.db = db_connection
    install_extensions(db_connection, ["uuid-ossp"])
    Session.create_table()
    session_id = uuid.uuid4()

    raw_request = bytes(f"GET / HTTP/1.1\nCookie: session_id={session_id}\n", "utf-8")
    request = HttpRequest(raw_request)

    with pytest.raises(SessionDoesNotExist):
        get_current_session(request)
