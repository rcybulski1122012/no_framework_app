from app.core.errors import Http404, SessionDoesNotExist
from app.core.http.sessions import get_current_session
from app.core.shortcuts import render_static, render_template
from app.settings import ACCEPTED_STATIC_MIME_TYPES


def index(request):
    try:
        get_current_session(request)
    except SessionDoesNotExist:
        return render_template(request, "authentication.html")
    else:
        return render_template(request, "index.html")


def static(request, file_name):
    try:
        file_type = file_name.split(".", 1)[1]
        MIME_type = ACCEPTED_STATIC_MIME_TYPES[file_type]
    except (IndexError, KeyError):
        raise Http404

    return render_static(request, MIME_type, file_name)
