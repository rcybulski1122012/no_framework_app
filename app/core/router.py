from app.core.errors import Http404


class Router:
    def __init__(self):
        self.views = {}

    def register_view(self, path, MIME_type=None):
        def wrap(func):
            func.MIME_type = MIME_type
            self.views[path] = func
            return func

        return wrap

    def route(self, path):
        try:
            return self.views[path]
        except KeyError:
            raise Http404
