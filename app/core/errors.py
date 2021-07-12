import json

from app.core.http.response import HttpResponse


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


class MissingEnvironmentVariable(Exception):
    pass
