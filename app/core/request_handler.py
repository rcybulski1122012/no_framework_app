from app.core.errors import Http400, Http404
from app.core.request_parser import HttpRequest


class RequestHandler:
    def __init__(self, router):
        self.router = router

    def __call__(self, request):
        try:
            request = HttpRequest(request)
        except Http400:
            return b"HTTP/1.1 400 BAD REQUEST\n"

        return self._handle_request(request)

    def _handle_request(self, request):
        try:
            view = self.router.route(request.path)
        except Http404:
            return f"{request.version} 404 NOT FOUND\n".encode("utf-8")

        response = view(request)
        http_response = f"{request.version} 200 OK\n\n{response}"
        return http_response.encode("utf-8")
