import traceback

from app.core.http.errors import Http404, HttpException, InvalidRequestFormat
from app.core.http.request import HttpRequest
from app.core.http.response import HttpResponse


class RequestHandler:
    def __init__(self, router):
        self.router = router

    def __call__(self, request):
        try:
            request = HttpRequest(request)
        except InvalidRequestFormat as e:
            return e.get_response().get_bytes()

        try:
            return self._handle_request(request)
        except HttpException as e:
            return e.get_response(request).get_bytes()
        except Exception as e:
            print(f"[ERROR]:{e}")
            traceback.print_exc()
            return HttpResponse("HTTP/1.1", 500, "Internal Server Error").get_bytes()

    def _handle_request(self, request):
        try:
            view, kwargs = self.router.route(request.path)
        except Http404 as e:
            return e.get_response(request).get_bytes()

        response = view(request, **kwargs)
        return response.get_bytes()
