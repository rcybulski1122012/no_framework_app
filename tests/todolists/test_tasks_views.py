import json

import pytest

from app.core.errors import Http401, Http403, Http404
from app.core.http.request import HttpRequest
from app.todolists.models import Task, ToDoList
from app.todolists.tasks_views import tasks_list_view


def test_tasks_list_view_returns_list_of_tasks(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    task1 = Task.create(content="first", todolist_id=todolist.id_)
    task2 = Task.create(content="second", todolist_id=todolist.id_)
    expected = {
        "tasks": [
            task1.get_fields_values_dict(),
            task2.get_fields_values_dict(),
        ]
    }
    request = HttpRequest(
        f"GET /tasks/1 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )
    response = tasks_list_view(request, todolist.id_)
    result = json.loads(response.body)

    assert expected == result


def test_tasks_list_view_raises_401_when_unauthorized(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)

    request = HttpRequest(
        f"GET /tasks/1 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )

    with pytest.raises(Http401):
        tasks_list_view(request, todolist.id_)


def test_tasks_list_view_raises_403_when_not_logged_in():
    request = HttpRequest(f"GET /tasks/1 HTTP/1.1\n".encode())

    with pytest.raises(Http403):
        tasks_list_view(request, 1)


def test_tasks_list_view_raises_404_when_todolist_does_not_exist(user_and_session):
    user, session = user_and_session
    request = HttpRequest(
        f"GET /tasks/1 HTTP/1.1\nCookie: session_id={session.session_id}\n".encode()
    )

    with pytest.raises(Http404):
        tasks_list_view(request, 1)
