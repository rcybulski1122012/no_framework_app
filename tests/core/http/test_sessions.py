import pytest
from uuid import UUID

from app.core.db.model import Model
from app.core.errors import InvalidSessionData
from app.core.http.sessions import Session


def test_session_dunder_init_when_json_string_given():
    session = Session(data='{"bar":["baz", null, 1.0, 2]}')
    expected = {'bar': ['baz', None, 1.0, 2]}

    assert session.json_data == expected


def test_session_dunder_init_when_dict_given():
    session = Session(data={'bar': ['baz', None, 1.0, 2]})
    expected = {'bar': ['baz', None, 1.0, 2]}

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

