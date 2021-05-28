import re
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

        try:
            self._parse(request_string)
        except Exception:
            raise Http400

    def _parse(self, request_string):
        pattern = re.compile(r"([a-zA-z]*) (/[a-zA-Z0-9.-/?&=]*) (HTTP/\d.\d)\n"
                             r"((.+\s*:\s*.+\s*\n)*)"
                             r"\n*([.\n]*)")

        match = pattern.match(request_string)
        self.method, path, self.version, headers_string, _, self.body = match.groups()
        self._parse_path(path)
        self._parse_headers(headers_string)

    def _parse_path(self, path):
        try:
            self.path, params = path.split("?", 1)
        except ValueError:
            self.path = path
        else:
            params = params.split("&")
            for param in params:
                key, val = param.split("=")
                self.params[key] = val

    def _parse_headers(self, headers_string):
        for header in headers_string.strip().split("\n"):
            key, val = [string.strip() for string in header.split(":", 1)]
            self.headers[key] = val
