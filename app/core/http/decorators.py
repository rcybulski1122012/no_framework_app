from functools import wraps

from app.core.http.errors import Http405


def http_method_required(method):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.method.lower() == method.lower():
                return func(request, *args, **kwargs)
            else:
                raise Http405

        return wrapper

    return decorator
