from app.core.errors import SessionDoesNotExist
from app.core.http.sessions import get_current_session
from app.core.shortcuts import render_template, render_static

STATIC_MIME_TYPES = {"css": "text/css", "js": "text/javascript"}


def index(request):
    try:
        get_current_session(request)
    except SessionDoesNotExist:
        return render_template(request, "authentication.html")
    else:
        return render_template(request, "index.html")


def static(request, file_name,):
    file_type = file_name.split(".", 1)[1]
    MIME_type = STATIC_MIME_TYPES[file_type]
    return render_static(request, MIME_type, file_name)
