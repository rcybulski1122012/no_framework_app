import json

from app.auth.errors import (AuthenticationError, PasswordsDoNotMatch,
                             TakenEmailError, TakenUsernameError)
from app.auth.models import AppUser
from app.auth.shortcuts import authenticate
from app.core.errors import Http400
from app.core.http.decorators import http_method_required
from app.core.http.response import HttpResponse
from app.core.http.sessions import Session
from app.core.shortcuts import json_response


@http_method_required("POST")
def create_user_view(request):
    username, password1, password2, email = _get_registration_data(request)

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


def _get_registration_data(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        password1 = data["password1"]
        password2 = data["password2"]
        email = data["email"]
    except (json.decoder.JSONDecodeError, KeyError):
        raise Http400

    return username, password1, password2, email


@http_method_required("POST")
def login_user_view(request):
    username, password = _get_login_data(request)

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


def _get_login_data(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
    except (json.decoder.JSONDecodeError, KeyError):
        raise Http400

    return username, password
