from app.auth.models import AppUser
from app.todolists.models import Task, ToDoList


def test_todolist_creator_property_returns_creator():
    user = AppUser(username="username", password="password", email="email@gmail.com")
    user.save()

    todolist = ToDoList(name="name", creator_id=user.id_)
    todolist.save()

    assert str(user) == str(todolist.creator)


def test_todolist_tasks_property_returns_tasks():
    todolist = ToDoList(name="name", creator_id=1)
    todolist.save()
    task1 = Task(content="task 1", todolist_id=todolist.id_)
    task1.save()
    task2 = Task(content="task 2", todolist_id=todolist.id_)
    task2.save()

    result = todolist.tasks
    expected = [task1, task2]

    assert str(result) == str(expected)


def test_task_todolist_property_returns_todolist():
    todolist = ToDoList(name="name", creator_id=1)
    todolist.save()
    task = Task(content="task", todolist_id=todolist.id_)
    task.save()

    assert str(todolist) == str(task.todolist)
