import json

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


class ValidationError(Exception):
    def get_response(self, request):
        body = json.dumps({"error": self.error_message})
        headers = {"Content-Type": "application/json", "Content-Length": len(body)}
        return HttpResponse(request.version, 400, "Bad Request", headers, body)

    @property
    def error_message(self):
        try:
            return self.args[0]
        except IndexError:
            return ""
