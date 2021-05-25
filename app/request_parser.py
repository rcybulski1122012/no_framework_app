class InvalidHttpRequest(Exception):
    pass


class HttpRequest:
    def __init__(self, request_string):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = ""
        self.request_string = request_string.strip()

        try:
            self._parse_request_line(self.request_string)
            self._parse_headers(self.request_string)
            self._parse_body(self.request_string)
        except Exception:
            raise InvalidHttpRequest

    def _parse_request_line(self, request_string):
        request_line = request_string.split("\n")[0]
        self.method, self.path, self.version = request_line.split()

    def _parse_headers(self, request_string):
        request_string = request_string.split("\n")

        try:
            end_of_headers = request_string.index("")
        except ValueError:
            end_of_headers = None

        headers_strings = request_string[1:end_of_headers]
        for header_string in headers_strings:
            colon_index = header_string.index(":")
            key, value = header_string[:colon_index], header_string[colon_index+2:]
            self.headers[key] = value

    def _parse_body(self, request_string):
        request_string = request_string.split("\n")
        try:
            end_of_headers = request_string.index("")
        except ValueError:
            pass
        else:
            self.body = "\n".join(request_string[end_of_headers:]).strip()
