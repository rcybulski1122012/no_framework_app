import uuid
from uuid import UUID

import pytest

from app.core.db.model import Model
from app.core.http.errors import Http403, InvalidSessionData
from app.core.http.request import HttpRequest
from app.core.http.sessions import Session, get_current_session_or_403
from app.scripts.install_extensions import install_extensions


def test_session_dunder_init_when_json_string_given():
    session = Session(data='{"bar":["baz", null, 1.0, 2]}')
    expected = {"bar": ["baz", None, 1.0, 2]}

    assert session.json_data == expected


def test_session_dunder_init_when_dict_given():
    session = Session(data={"bar": ["baz", None, 1.0, 2]})
    expected = {"bar": ["baz", None, 1.0, 2]}

    assert session.json_data == expected


def test_session_dunder_init_when_given_foreign_type_raises_exception():
    with pytest.raises(InvalidSessionData):
        Session(data=["a", "b"])


def test_session_dunder_init_when_given_string_cant_be_converted_into_dict():
    with pytest.raises(InvalidSessionData):
        Session(data='["foo", {"bar":["baz", null, 1.0, 2]}]')


def test_session_dunder_getitem():
    session = Session(data='{"first": 5, "second": 10}')
    result = session["first"]
    expected = 5

    assert result == expected


def test_session_dunder_setitem():
    session = Session(data='{"first": 5, "second": 10}')
    expected = session["first"] = 50
    result = session["first"]

    assert result == expected


def test_session_save_convert_json_data_to_string(monkeypatch):
    monkeypatch.setattr(Model, "save", lambda self: None)
    session = Session(data='{"first": 5, "second": 10}')
    expected = '{"first": 5, "second": 10, "third": 15}'
    session["third"] = 15
    session.save()

    assert session.data == expected


def test_session_dunder_init_generates_session_id_if_no_provided():
    session = Session(data='{"first": 5, "second": 10}')
    result = session.session_id

    assert isinstance(result, UUID)


def test_get_current_session_returns_session(db_connection):
    Session.db = db_connection
    install_extensions(db_connection, ["uuid-ossp"])
    Session.create_table()
    session = Session(data='{"user_id": 1}')
    session.save()
    session = Session.select()[0]
    raw_request = bytes(
        f"GET / HTTP/1.1\nCookie: session_id={session.session_id}\n", "utf-8"
    )
    request = HttpRequest(raw_request)
    result = get_current_session_or_403(request)

    assert str(result) == str(session)


def test_get_current_session_raises_exception_when_session_id_not_in_cookie():
    raw_request = bytes(f"GET / HTTP/1.1\n", "utf-8")
    request = HttpRequest(raw_request)

    with pytest.raises(Http403):
        get_current_session_or_403(request)


def test_get_current_session_raises_exception_when_session_not_id_db(db_connection):
    Session.db = db_connection
    install_extensions(db_connection, ["uuid-ossp"])
    Session.create_table()
    session_id = uuid.uuid4()

    raw_request = bytes(f"GET / HTTP/1.1\nCookie: session_id={session_id}\n", "utf-8")
    request = HttpRequest(raw_request)

    with pytest.raises(Http403):
        get_current_session_or_403(request)
