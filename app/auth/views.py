import json

from app.auth.errors import PasswordsDoNotMatch, UserDoesNotExist
from app.auth.models import AppUser
from app.auth.shortcuts import authenticate
from app.core.errors import Http400
from app.core.http.decorators import POST_required
from app.core.http.response import HttpResponse
from app.core.http.sessions import Session
from app.core.shortcuts import json_response


@POST_required
def create_user_view(request):
    username, password1, password2, email = _get_registration_data(request)

    if password1 != password2:
        response_body = {"error": "Both passwords should be the same."}
    elif AppUser.select(username=username):
        response_body = {"error": "This username is taken."}
    elif AppUser.select(email=email):
        response_body = {"error": "An account with this email already exists."}
    else:
        user = AppUser(username=username, password=password1, email=email)
        user.save()
        return HttpResponse(request.version, 201, "Created", {}, '{}')

    return json_response(request, response_body)


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


@POST_required
def login_user_view(request):
    username, password = _get_login_data(request)

    try:
        user = authenticate(username, password)
    except UserDoesNotExist:
        response_body = {"error": "User with this username does not exist."}
    except PasswordsDoNotMatch:
        response_body = {"error": "Invalid password."}
    else:
        data = json.dumps({"user_id": user.id_})
        session = Session(data=data)
        session.save()
        body = json.dumps({"session_id": str(session.session_id)})
        # todo refactor json_response, optional after * parameter status code
        return HttpResponse(request.version, 201, "Created", {"Content-Type": "application/json"}, body)

    return json_response(request, response_body)


def _get_login_data(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
    except (json.decoder.JSONDecodeError, KeyError):
        raise Http400

    return username, password
