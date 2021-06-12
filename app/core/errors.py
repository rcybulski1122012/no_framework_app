from app.core.http.response import HttpResponse


class HttpException(Exception):
    pass


class Http400(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 400, "Bad Request").get_response()


class Http404(HttpException):
    @staticmethod
    def get_response(request):
        return HttpResponse(request.version, 404, "Not Found").get_response()


class MissingEnvironmentVariable(Exception):
    pass


class MissingRequiredArgument(Exception):
    pass


class ModelDeletionException(Exception):
    pass


class SessionDoesNotExist(Exception):
    pass


class InvalidCondition(Exception):
    pass


class InvalidSessionData(Exception):
    pass
