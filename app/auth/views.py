import json

from app.auth.models import AppUser
from app.auth.shortcuts import authenticate
from app.core.errors import ValidationError
from app.core.http.decorators import http_method_required
from app.core.http.response import HttpResponse
from app.core.http.sessions import Session, get_current_session_or_403
from app.core.shortcuts import get_data_from_request_body, json_response, redirect


@http_method_required("POST")
def create_user_view(request):
    username, password1, password2, email = get_data_from_request_body(
        request, ["username", "password1", "password2", "email"]
    )

    try:
        _validate_registration_data(username, password1, password2, email)
        user = AppUser(username=username, password=password1, email=email)
    except ValidationError as e:
        return e.get_response(request)

    user.save()
    return HttpResponse(request.version, 201, "Created", {}, "{}")


def _validate_registration_data(username, password1, password2, email):
    if password1 != password2:
        raise ValidationError("Both passwords should be the same.")
    elif AppUser.select(username=username):
        raise ValidationError("This username is taken.")
    elif AppUser.select(email=email):
        raise ValidationError("An account with this email already exists.")


@http_method_required("POST")
def login_user_view(request):
    username, password = get_data_from_request_body(request, ["username", "password"])

    try:
        user = authenticate(username, password)
    except ValidationError as e:
        return e.get_response(request)

    data = json.dumps({"user_id": user.id_})
    session = Session(data=data)
    session.save()
    return json_response(
        request, {"session_id": str(session.session_id)}, status_code=201
    )


def logout_view(request):
    session = get_current_session_or_403(request)
    session.delete()

    return redirect(request, "/")
