from functools import wraps

from app.core.http.response import HttpResponse


def POST_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(request.version, 405, "Method Not Allowed")

    return wrapper
