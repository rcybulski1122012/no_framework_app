from app.core.http.response import HttpResponse


class HttpException(Exception):
    pass


class Http400(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 400, "Bad Request")


class Http401(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 401, "Unauthorized")


class Http403(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 403, "Forbidden")


class Http404(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 404, "Not Found")


class Http405(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 405, "Method Not Allowed")


class InvalidSessionData(Exception):
    pass


class InvalidRequestFormat(Exception):
    @staticmethod
    def get_response():
        return HttpResponse("HTTP/1.1", 400, "Bad Request")
