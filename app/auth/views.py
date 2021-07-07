import json

from app.auth.errors import (AuthenticationError, PasswordsDoNotMatch,
                             TakenEmailError, TakenUsernameError)
from app.auth.models import AppUser
from app.auth.shortcuts import authenticate
from app.core.http.decorators import http_method_required
from app.core.http.response import HttpResponse
from app.core.http.sessions import Session
from app.core.shortcuts import get_data_from_request_body, json_response


@http_method_required("POST")
def create_user_view(request):
    username, password1, password2, email = get_data_from_request_body(
        request, ["username", "password1", "password2", "email"]
    )

    try:
        _validate_registration_data(username, password1, password2, email)
    except AuthenticationError as e:
        return e.get_response(request)
    else:
        user = AppUser(username=username, password=password1, email=email)
        user.save()
        return HttpResponse(request.version, 201, "Created", {}, "{}")


def _validate_registration_data(username, password1, password2, email):
    if password1 != password2:
        raise PasswordsDoNotMatch
    elif AppUser.select(username=username):
        raise TakenUsernameError
    elif AppUser.select(email=email):
        raise TakenEmailError


@http_method_required("POST")
def login_user_view(request):
    username, password = get_data_from_request_body(request, ["username", "password"])

    try:
        user = authenticate(username, password)
    except AuthenticationError as e:
        return e.get_response(request)
    else:
        data = json.dumps({"user_id": user.id_})
        session = Session(data=data)
        session.save()
        return json_response(
            request, {"session_id": str(session.session_id)}, status_code=201
        )
