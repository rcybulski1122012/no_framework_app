from app.core.errors import Http403, SessionDoesNotExist
from app.core.http.sessions import get_current_session
from app.core.shortcuts import json_response
from app.todolists.models import ToDoList


def todolists_list_view(request):
    try:
        session = get_current_session(request)
    except SessionDoesNotExist:
        raise Http403

    todolists = ToDoList.select(creator_id=session["user_id"])
    serialized = [obj.get_fields_values_dict() for obj in todolists]
    response_dict = {"todolists": serialized}

    return json_response(request, response_dict)
