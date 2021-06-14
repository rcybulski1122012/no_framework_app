import json

from app.auth.models import AppUser
from app.core.http.request import HttpRequest
from app.core.http.sessions import Session
from app.todolists.models import ToDoList
from app.todolists.views import todolists_list_view


def test_todolists_list_view_returns_list_of_todolists():
    user = AppUser(username="username", password="password", email="email")
    user.save()
    todolist1 = ToDoList(name="first", creator_id=user.id_)
    todolist1.save()
    todolist2 = ToDoList(name="second", creator_id=user.id_)
    todolist2.save()
    session = Session(data=f'{{"user_id": {user.id_}}}')
    session.save()

    expected = {
        "todolists": [
            todolist1.get_fields_values_dict(),
            todolist2.get_fields_values_dict(),
        ]
    }
    raw_request = f"GET /users/{user.id_}/todolists HTTP/1.1\nCookie: session_id={session.session_id}\n\n"
    request = HttpRequest(bytes(raw_request, "utf-8"))

    response = todolists_list_view(request, user.id_)
    result = json.loads(response.body)

    assert result == expected


def test_todolists_list_view_returns_403_when_forbidden():
    session = Session(data='{"user_id": 1}')
    session.save()
    raw_request = (
        f"GET /users/1/todolists HTTP/1.1\nCookie: session_id={session.session_id}\n\n"
    )
    request = HttpRequest(bytes(raw_request, "utf-8"))

    response = todolists_list_view(request, 15)

    assert response.status_code == 403
