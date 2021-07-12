import json

import pytest

from app.core.http.errors import Http400, Http401, Http403, Http404, Http405
from app.core.http.request import HttpRequest
from app.todolists.models import Task, ToDoList
from app.todolists.tasks_views import (create_task_view, delete_task_view,
                                       mark_task_as_done_view, tasks_list_view)


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
    request = HttpRequest.create("GET", "/tasks/1", "HTTP/1.1", session)
    response = tasks_list_view(request, todolist.id_)
    result = json.loads(response.body)

    assert expected == result


def test_tasks_list_view_raises_401_when_unauthorized(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    request = HttpRequest.create("GET", "/tasks/1", "HTTP/1.1", session)

    with pytest.raises(Http401):
        tasks_list_view(request, todolist.id_)


def test_tasks_list_view_raises_403_when_not_logged_in():
    request = HttpRequest.create("GET", "/tasks/1", "HTTP/1.1")

    with pytest.raises(Http403):
        tasks_list_view(request, 1)


def test_tasks_list_view_raises_404_when_todolist_does_not_exist(user_and_session):
    user, session = user_and_session
    request = HttpRequest.create("GET", "/tasks/1", "HTTP/1.1", session)

    with pytest.raises(Http404):
        tasks_list_view(request, 1)


def test_create_task_view_creates_task(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    data = {"content": "content", "todolist_id": todolist.id_}
    request = HttpRequest.create("POST", "/create_task", "HTTP/1.1", session, data)

    before = Task.select()
    assert len(before) == 0

    create_task_view(request)

    after = Task.select()
    assert len(after) == 1

    task = after[0]
    assert task.content == "content"
    assert task.todolist_id == todolist.id_


def test_create_task_view_raises_400_when_invalid_data(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    data = {"todolist_id": todolist.id_}
    request = HttpRequest.create("POST", "/create_task", "HTTP/1.1", session, data)

    with pytest.raises(Http400):
        create_task_view(request)


def test_create_task_view_raises_401_when_unauthorized(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    data = {"content": "content", "todolist_id": todolist.id_}
    request = HttpRequest.create("POST", "/create_task", "HTTP/1.1", session, data)

    with pytest.raises(Http401):
        create_task_view(request)


def test_create_task_view_raises_403_when_not_logged_in():
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    data = {"content": "content", "todolist_id": todolist.id_}
    request = HttpRequest.create("POST", "/create_task", "HTTP/1.1", body=data)

    with pytest.raises(Http403):
        create_task_view(request)


def test_create_task_view_raises_404_when_todolist_does_not_exists(user_and_session):
    user, session = user_and_session
    data = {"content": "content", "todolist_id": 100}
    request = HttpRequest.create("POST", "/create_task", "HTTP/1.1", session, data)

    with pytest.raises(Http404):
        create_task_view(request)


def test_create_task_view_raises_405_when_method_different_than_POST():
    request = HttpRequest.create("GET", "/create_todolist", "HTTP/1.1")

    with pytest.raises(Http405):
        create_task_view(request)


def test_delete_task_view_deletes_task(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    task = Task.create(content="content", todolist_id=todolist.id_)
    request = HttpRequest.create("POST", "/delete_task/1", "HTTP/1.1", session)
    delete_task_view(request, task.id_)

    assert len(todolist.tasks) == 0


def test_delete_task_view_raises_401_when_unauthorized(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    task = Task.create(content="content", todolist_id=todolist.id_)
    request = HttpRequest.create("POST", "/delete_task/1", "HTTP/1.1", session)

    with pytest.raises(Http401):
        delete_task_view(request, task.id_)


def test_delete_task_view_raises_403_when_not_logged_in():
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    task = Task.create(content="content", todolist_id=todolist.id_)
    request = HttpRequest.create("POST", "/delete_task/1", "HTTP/1.1")

    with pytest.raises(Http403):
        delete_task_view(request, task.id_)


def test_delete_task_view_raises_404_when_task_does_not_exist(user_and_session):
    user, session = user_and_session
    request = HttpRequest.create("POST", "/delete_task/1", "HTTP/1.1", session)

    with pytest.raises(Http404):
        delete_task_view(request, 100)


def test_delete_task_view_raises_405_when_method_different_than_POST():
    request = HttpRequest.create("GET", "/delete_task/1", "HTTP/1.1")

    with pytest.raises(Http405):
        delete_task_view(request, 100)


def test_mark_task_as_done_view_marks_as_done(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(
        name="name", description="description", creator_id=user.id_
    )
    task = Task.create(content="content", todolist_id=todolist.id_)
    request = HttpRequest.create("POST", "/mark_task_as_done/10", "HTTP/1.1", session)

    assert not task.is_done

    mark_task_as_done_view(request, task.id_)
    task.refresh()

    assert task.is_done


def test_mark_task_as_done_view_raises_401_when_unauthorized(user_and_session):
    user, session = user_and_session
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    task = Task.create(content="content", todolist_id=todolist.id_)
    request = HttpRequest.create("POST", "/mark_task_as_done/10", "HTTP/1.1", session)

    with pytest.raises(Http401):
        mark_task_as_done_view(request, task.id_)


def test_mark_task_as_done_view_raises_403_when_not_logged_in():
    todolist = ToDoList.create(name="name", description="description", creator_id=100)
    task = Task.create(content="content", todolist_id=todolist.id_)
    request = HttpRequest.create("POST", "/mark_task_as_done/10", "HTTP/1.1")

    with pytest.raises(Http403):
        mark_task_as_done_view(request, task.id_)


def test_mark_task_as_done_view_raises_404_when_task_does_not_exist(user_and_session):
    user, session = user_and_session
    request = HttpRequest.create("POST", "/mark_task_as_done/10", "HTTP/1.1", session)

    with pytest.raises(Http404):
        mark_task_as_done_view(request, 100)


def test_mark_task_as_done_view_raises_405_when_method_different_than_POST():
    request = HttpRequest.create("GET", "/mark_task_as_done/10", "HTTP/1.1")

    with pytest.raises(Http405):
        mark_task_as_done_view(request, 100)
