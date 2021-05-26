from app.core.errors import Http400, Http404
from app.core.request_parser import HttpRequest
from app.core.response import HttpResponse


class RequestHandler:
    def __init__(self, router):
        self.router = router

    def __call__(self, request):
        try:
            request = HttpRequest(request)
        except Http400:
            return HttpResponse("HTTP/1.1", 400, "Bad Request").get_response()

        try:
            return self._handle_request(request)
        except Exception:
            return HttpResponse("HTTP/1.1", 500, "Internal Server Error").get_response()

    def _handle_request(self, request):
        try:
            view = self.router.route(request.path)
        except Http404:
            return HttpResponse(request.version, 404, "Not Found").get_response()

        body = view(request)
        headers = self.get_headers(body, view)
        response = HttpResponse(request.version, 200, "OK", headers, body)
        return response.get_response()

    def get_headers(self, body, view):
        if body and view.MIME_type:
            return {
                "Content-Type": view.MIME_type,
                "Content-Length": len(body)
            }
        return None
