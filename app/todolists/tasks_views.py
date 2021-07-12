from app.core.http.decorators import http_method_required
from app.core.http.errors import Http401
from app.core.http.response import HttpResponse
from app.core.http.sessions import get_current_session_or_403
from app.core.shortcuts import (get_data_from_request_body, get_object_or_404,
                                json_response)
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


@http_method_required("POST")
def create_task_view(request):
    session = get_current_session_or_403(request)
    content, todolist_id = get_data_from_request_body(
        request, ["content", "todolist_id"]
    )
    todolist = get_object_or_404(ToDoList, id_=todolist_id)

    if todolist.creator_id != session["user_id"]:
        raise Http401

    task = Task.create(content=content, todolist_id=todolist_id)

    return json_response(
        request, task.get_fields_values_dict(), status_code=201, readable="Created"
    )


@http_method_required("POST")
def delete_task_view(request, id_):
    session = get_current_session_or_403(request)
    task = get_object_or_404(Task, id_=id_)
    todolist = task.todolist

    if todolist.creator_id != session["user_id"]:
        raise Http401

    task.delete()

    return HttpResponse(request.version, 200, "OK")


@http_method_required("POST")
def mark_task_as_done_view(request, id_):
    session = get_current_session_or_403(request)
    task = get_object_or_404(Task, id_=id_)
    todolist = task.todolist

    if todolist.creator_id != session["user_id"]:
        raise Http401

    task.is_done = True
    task.save()

    return HttpResponse(request.version, 200, "OK")
