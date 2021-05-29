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
        except Exception as e:
            print(f"[ERROR]:{e}")
            return HttpResponse("HTTP/1.1", 500, "Internal Server Error").get_response()

    def _handle_request(self, request):
        try:
            view, kwargs = self.router.route(request.path)
        except Http404:
            return HttpResponse(request.version, 404, "Not Found").get_response()

        body, MIME_type = view(request, **kwargs)
        headers = self.get_headers(body, MIME_type)
        response = HttpResponse(request.version, 200, "OK", headers, body)
        return response.get_response()

    def get_headers(self, body, MIME_type):
        if body and MIME_type:
            return {
                "Content-Type": MIME_type,
                "Content-Length": len(body),
            }
        return None
