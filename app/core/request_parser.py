from app.core.errors import Http400
from app.core.utils import CaseInsensitiveDict


class HttpRequest:
    def __init__(self, request_string):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = CaseInsensitiveDict()
        self.body = ""
        self.params = {}

        request_string = request_string.replace(b"\r", b"").decode("utf-8")
        self.request_string = request_string.strip()

        try:
            self._parse_request_line(self.request_string)
            self._parse_GET_arguments()
            self._parse_headers(self.request_string)
            self._parse_body(self.request_string)
        except Exception:
            raise Http400

    def _parse_request_line(self, request_string):
        request_line = request_string.split("\n")[0]
        self.method, self.path, self.version = request_line.split()

    def _parse_GET_arguments(self):
        try:
            self.path, args = self.path.split("?", 1)
            for arg in args.split("&"):
                name, value = arg.split("=")
                self.params[name] = value
        except ValueError:
            pass

    def _parse_headers(self, request_string):
        request_string = request_string.split("\n")

        try:
            end_of_headers = request_string.index("")
        except ValueError:
            end_of_headers = None

        headers_strings = request_string[1:end_of_headers]
        for header_string in headers_strings:
            header, value = [string.strip() for string in header_string.split(":", 1)]
            self.headers[header] = value

    def _parse_body(self, request_string):
        request_string = request_string.split("\n")
        try:
            end_of_headers = request_string.index("")
        except ValueError:
            pass
        else:
            self.body = "\n".join(request_string[end_of_headers:]).strip()
