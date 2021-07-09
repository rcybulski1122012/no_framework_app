from app.core.errors import Http401
from app.core.http.sessions import get_current_session_or_403
from app.core.shortcuts import get_object_or_404, json_response
from app.todolists.models import Task, ToDoList


def tasks_list_view(request, todolist_id):
    session = get_current_session_or_403(request)
    todolist = get_object_or_404(ToDoList, id_=todolist_id)

    if todolist.creator_id != session["user_id"]:
        raise Http401

    tasks = Task.select(todolist_id=todolist_id)
    serialized = [obj.get_fields_values_dict() for obj in tasks]
    response_dict = {"tasks": serialized}

    return json_response(request, response_dict)
