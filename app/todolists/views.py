from app.core.http.response import HttpResponse
from app.core.http.sessions import get_current_session
from app.core.shortcuts import json_response
from app.todolists.models import ToDoList


def todolists_list_view(request, user_id):
    session = get_current_session(request)

    if session["user_id"] != user_id:
        return HttpResponse(request.version, 403, "Forbidden")

    todolists = ToDoList.select(creator_id=user_id)
    serialized = [obj.get_fields_values_dict() for obj in todolists]
    response_dict = {"todolists": serialized}

    return json_response(request, response_dict)
