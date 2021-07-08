import pytest

from app.auth.models import AppUser
from app.core.errors import ValidationError
from app.todolists.models import Task, ToDoList


def test_todolist_creator_property_returns_creator():
    user = AppUser.create(
        username="username", password="Password0!", email="email@gmail.com"
    )

    todolist = ToDoList(name="name", creator_id=user.id_)
    todolist.save()

    assert str(user) == str(todolist.creator)


def test_todolist_tasks_property_returns_tasks():
    todolist = ToDoList.create(name="name", creator_id=1)
    task1 = Task.create(content="task 1", todolist_id=todolist.id_)
    task2 = Task.create(content="task 2", todolist_id=todolist.id_)

    result = todolist.tasks
    expected = [task1, task2]

    assert str(result) == str(expected)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"name": "", "description": "description", "creator_id": 1},
        {"name": "a" * 65, "description": "description", "creator_id": 1},
        {"name": "aaaa", "description": "a" * 257, "creator_id": 1},
    ],
)
def test_todolist_validation(kwargs):
    with pytest.raises(ValidationError):
        ToDoList(**kwargs)


def test_task_todolist_property_returns_todolist():
    todolist = ToDoList.create(name="name", creator_id=1)
    task = Task.create(content="task", todolist_id=todolist.id_)

    assert str(todolist) == str(task.todolist)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"content": "", "todolist_id": 1},
        {"content": "a" * 129, "todolist_id": 1},
    ],
)
def test_task_validation(kwargs):
    with pytest.raises(ValidationError):
        Task(**kwargs)
