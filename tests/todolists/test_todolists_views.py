import json
import uuid

import pytest

from app.core.http.errors import Http400, Http401, Http403, Http404, Http405
from app.core.http.request import HttpRequest
from app.core.http.sessions import Session
from app.todolists.models import ToDoList
from app.todolists.todolists_views import (create_todolist_view,
                                           delete_todolist_view,
                                           edit_todolist_view,
                                           todolists_list_view,
                                           update_todolist_view)
from tests.utils import json_request


def test_todolists_list_view_returns_list_of_todolists(user_and_session):
    user, session = user_and_session
    todolist1 = ToDoList.create(name="first", creator_id=user.id_)
    todolist2 = ToDoList.create(name="second", creator_id=user.id_)

    expected = {
        "todolists": [
            todolist1.get_fields_values_dict(),
            todolist2.get_fields_values_dict(),
        ]
    }
    request = HttpRequest(
        f"GET /create_todolist HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )
    response = todolists_list_view(request)
    result = json.loads(response.body)

    assert result == expected


def test_todolists_list_view_raises_401_when_not_logged_in():
    request = HttpRequest(f"GET /todolist HTTP/1.1\n".encode())

    with pytest.raises(Http403):
        todolists_list_view(request)


def test_create_todolist_view_creates_todolist(user_and_session):
    user, session = user_and_session
    data = {"name": "name", "description": "description"}
    request = json_request("POST", "/create_todolist", data, session)

    before = ToDoList.select()
    assert len(before) == 0

    create_todolist_view(request)

    after = ToDoList.select()
    assert len(after) == 1
    todolist = after[0]

    assert todolist.creator_id == user.id_
    assert todolist.name == "name"
    assert todolist.description == "description"


def test_create_todolist_view_returns_error_when_invalid_data(user_and_session):
    user, session = user_and_session
    data = {"name": "", "description": "description"}
    request = json_request("POST", "/create_todolist", data, session)

    response = create_todolist_view(request)

    assert "error" in response.body


def test_create_todolist_view_returns_json_repr_of_created_list(user_and_session):
    user, session = user_and_session
    data = {"name": "name", "description": "description"}
    request = json_request("POST", "/create_todolist", data, session)
    response = create_todolist_view(request)
    result = json.loads(response.body)
    todolist = ToDoList.select()[0]

    assert result == todolist.get_fields_values_dict()


def test_create_todolist_view_raises_400_when_lack_of_data(user_and_session):
    user, session = user_and_session
    data = {"name": "name"}
    request = json_request("POST", "/create_todolist", data, session)

    with pytest.raises(Http400):
        create_todolist_view(request)


def test_create_todolist_view_raises_403_when_forbidden():
    session_id = uuid.uuid4()
    request = HttpRequest(
        f"POST /create_todolist HTTP/1.1\nCookie: session_id={session_id}\n".encode()
    )

    with pytest.raises(Http403):
        create_todolist_view(request)


def test_create_todolist_raises_405_when_method_different_than_POST():
    request = HttpRequest(f"GET /create_todolist HTTP/1.1\n".encode())

    with pytest.raises(Http405):
        create_todolist_view(request)


def test_delete_todolist_view_deletes_todolist(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    data = {"id_": todolist.id_}
    request = json_request("POST", "/delete_todolist", data, session)

    before = ToDoList.select()
    assert len(before) == 1

    response = delete_todolist_view(request, todolist.id_)

    after = ToDoList.select()
    assert len(after) == 0
    assert response.status_code == 200


def test_delete_todolist_view_raises_401_when_forbidden(user_and_session):
    user = user_and_session[0]
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    session = Session.create(data={"user_id": 100})

    request = HttpRequest(
        f"POST /delete_todolist/10 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )

    with pytest.raises(Http401):
        delete_todolist_view(request, todolist.id_)


def test_delete_todolist_raises_403_when_not_logged_in():
    request = HttpRequest(f"POST /delete_todolist/10 HTTP/1.1\n".encode())

    with pytest.raises(Http403):
        delete_todolist_view(request, 10)


def test_delete_todolist_view_raises_404_when_todolist_does_not_exist(user_and_session):
    user, session = user_and_session

    request = HttpRequest(
        f"POST /delete_todolist/10 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )

    with pytest.raises(Http404):
        delete_todolist_view(request, 100)


def test_delete_todolist_raises_405_when_method_different_than_POST():
    request = HttpRequest(f"GET /delete_todolist HTTP/1.1\n".encode())

    with pytest.raises(Http405):
        delete_todolist_view(request, 10)


def test_edit_todolist_view_returns_edit_todolist_html_template(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="test-todolist-name",
        description="test-todolist-description",
        creator_id=user.id_,
    )
    request = HttpRequest(
        f"GET /edit_todolist/10 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )
    response = edit_todolist_view(request, todolist.id_)

    assert "test-todolist-name" in response.body
    assert "test-todolist-description" in response.body
    assert response.status_code == 200


def test_edit_todolist_view_raises_401_when_forbidden(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    request = HttpRequest(
        f"GET /edit_todolist/10 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )

    with pytest.raises(Http401):
        edit_todolist_view(request, todolist.id_)


def test_edit_todolist_view_raises_404_when_todolist_does_not_exist(user_and_session):
    user, session = user_and_session
    request = HttpRequest(
        f"GET /edit_todolist/10 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )

    with pytest.raises(Http404):
        edit_todolist_view(request, 10)


def test_edit_todolist_view_redirects_to_index_not_logged_in():
    request = HttpRequest(f"GET /delete_todolist/10 HTTP/1.1\n".encode())

    response = edit_todolist_view(request, 10)

    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_update_todolist_view_updates_todolist(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    data = {"name": "new name", "description": "new description"}
    request = json_request("POST", "/update_todolist/10", data, session)

    update_todolist_view(request, todolist.id_)
    todolist = ToDoList.select(id_=todolist.id_)[0]

    assert todolist.name == "new name"
    assert todolist.description == "new description"


def test_update_todolist_view_returns_error_when_invalid_data(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    data = {"name": "", "description": "description"}
    request = json_request("POST", "/update_todolist/10", data, session)

    response = update_todolist_view(request, todolist.id_)

    assert "error" in response.body


def test_update_todolist_view_raises_400_when_lack_of_data(user_and_session):
    user, session = user_and_session
    data = {"name": "name"}
    request = json_request("POST", "/create_todolist", data, session)

    with pytest.raises(Http400):
        update_todolist_view(request, 10)


def test_update_todolist_view_raises_401_when_forbidden(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    data = {"name": "name", "description": "description"}
    request = json_request("POST", "/update_todolist/10", data, session)

    with pytest.raises(Http401):
        edit_todolist_view(request, todolist.id_)


def test_update_todolist_view_raises_403_when_not_logged_in():
    request = json_request(
        "POST", "/delete_todolist/10", {"name": "name", "description": "description"}
    )

    with pytest.raises(Http403):
        update_todolist_view(request, 10)


def test_update_todolist_view_raises_404_when_todolist_does_not_exists(
    user_and_session,
):
    user, session = user_and_session
    request = json_request(
        "POST",
        "/delete_todolist/10",
        {"name": "name", "description": "description"},
        session,
    )

    with pytest.raises(Http404):
        update_todolist_view(request, 10)


def test_update_todolist_view_raises_405_when_method_different_than_POST():
    request = HttpRequest(f"GET /update_todolist/10 HTTP/1.1\n".encode())

    with pytest.raises(Http405):
        update_todolist_view(request, 10)
