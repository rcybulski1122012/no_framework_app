import json

from app.core.http.errors import InvalidRequestFormat
from app.core.utils import CaseInsensitiveDict


class HttpRequest:
    def __init__(self, request_string):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = CaseInsensitiveDict()
        self.body = ""
        self.params = {}
        self.cookies = {}

        request_string = request_string.replace(b"\r", b"").decode("utf-8")
        self.request_string = request_string.strip()

        try:
            self._parse_request_line()
            self._parse_GET_arguments()
            self._parse_headers()
            self._parse_body()
            self._parse_cookies()
        except Exception:
            raise InvalidRequestFormat

    def _parse_request_line(self):
        request_line = self.request_string.split("\n")[0]
        self.method, self.path, self.version = request_line.split()

    def _parse_GET_arguments(self):
        try:
            self.path, args = self.path.split("?", 1)
            for arg in args.split("&"):
                name, value = arg.split("=")
                self.params[name] = value
        except ValueError:
            pass

    def _parse_headers(self):
        splitted_request = self.request_string.split("\n")
        end_of_headers = self._get_end_of_headers(splitted_request)

        headers_strings = splitted_request[1:end_of_headers]
        for header_string in headers_strings:
            header, value = [string.strip() for string in header_string.split(":", 1)]
            self.headers[header] = value

    def _parse_body(self):
        splitted_request = self.request_string.split("\n")
        end_of_headers = self._get_end_of_headers(splitted_request)
        if end_of_headers:
            self.body = "\n".join(splitted_request[end_of_headers:]).strip()

    @staticmethod
    def _get_end_of_headers(splitted_request):
        try:
            return splitted_request.index("")
        except ValueError:
            return None

    def _parse_cookies(self):
        try:
            cookies = self.headers["cookie"]
        except KeyError:
            return

        splitted = [string.strip() for string in cookies.split(";")]

        for cookie_str in splitted:
            key, value = cookie_str.split("=", 1)
            self.cookies[key] = value

    @classmethod
    def create(cls, method, path, version, session=None, body=None):
        raw_request = f"{method} {path} {version}\n"

        if session is not None:
            raw_request += f"Cookie: session_id={session.session_id}\n"

        if body is not None:
            body_str = json.dumps(body)
            raw_request += (
                f"Content-Type: application/json\n"
                f"Content-Length: {len(body_str)}\n\n"
                f"{body_str}"
            )

        return cls(raw_request.encode())
