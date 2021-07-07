from app.core.errors import Http403
from app.core.http.decorators import http_method_required
from app.core.http.sessions import get_current_session_or_403
from app.core.shortcuts import (get_data_from_request_body, json_response,
                                redirect, render_template)
from app.todolists.models import ToDoList


def todolists_list_view(request):
    session = get_current_session_or_403(request)

    todolists = ToDoList.select(creator_id=session["user_id"])
    serialized = [obj.get_fields_values_dict() for obj in todolists]
    response_dict = {"todolists": serialized}

    return json_response(request, response_dict)


@http_method_required("POST")
def create_todolist_view(request):
    session = get_current_session_or_403(request)

    name, description = get_data_from_request_body(request, ["name", "description"])
    todolist = ToDoList.create(
        name=name, description=description, creator_id=session["user_id"]
    )
    return json_response(request, todolist.get_fields_values_dict())


@http_method_required("POST")
def delete_todolist_view(request, id_):
    session = get_current_session_or_403(request)

    todolist = ToDoList.select(id_=id_)[0]
    if todolist.creator_id != session["user_id"]:
        raise Http403

    todolist.delete()

    return json_response(request, {})


def edit_todolist_view(request, id_):
    try:
        session = get_current_session_or_403(request)
    except Http403:
        return redirect(request, "/")

    todolist = ToDoList.select(id_=id_)[0]

    if todolist.creator_id != session["user_id"]:
        raise Http403

    return render_template(
        request,
        "edit_todolist.html",
        name=todolist.name,
        description=todolist.description,
        id_=id_,
    )


@http_method_required("POST")
def update_todolist_view(request, id_):
    session = get_current_session_or_403(request)

    todolist = ToDoList.select(id_=id_)[0]
    if todolist.creator_id != session["user_id"]:
        raise Http403

    name, description = get_data_from_request_body(request, ["name", "description"])

    todolist.name = name
    todolist.description = description
    todolist.save()

    return json_response(request, {})
