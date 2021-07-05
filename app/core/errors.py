from app.core.http.response import HttpResponse


class HttpException(Exception):
    pass


class Http400(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 400, "Bad Request")


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


class MissingEnvironmentVariable(Exception):
    pass


class MissingRequiredArgument(Exception):
    pass


class ModelDeletionException(Exception):
    pass


class InvalidCondition(Exception):
    pass


class InvalidSessionData(Exception):
    pass


class InvalidRequestFormat(Exception):
    pass
