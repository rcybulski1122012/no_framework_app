class HttpRequest:
    def __init__(self, request_string):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = ""

        self._parse_request_line(request_string)
        self._parse_headers(request_string)
        self._parse_body(request_string)

    def _parse_request_line(self, request_string):
        request_line = request_string.split("\n")[0]
        self.method, self.path, self.version = request_line.split()

    def _parse_headers(self, request_string):
        request_string = request_string.split("\n")

        try:
            end_of_headers = request_string.index("")
        except ValueError:
            end_of_headers = -1

        headers_strings = request_string[1:end_of_headers]
        for header_string in headers_strings:
            key, value = [string.strip() for string in header_string.split(":")]
            self.headers[key] = value

    def _parse_body(self, request_string):
        request_string = request_string.split("\n")
        print(request_string)
        try:
            end_of_headers = request_string.index("")
        except ValueError:
            pass
        else:
            self.body = "\n".join(request_string[end_of_headers:]).strip()


GET_request = ("GET /hello.htm HTTP/1.1\n"
               "Host: www.host.com\n"
               "Accept-Language: en-us\n")

POST_request = ("POST /cgi-bin/process.cgi HTTP/1.1\n"
                "Host: www.host.com\n"
                "Content-Type: application/x-www-form-urlencoded\n"
                "Content-Length: length\n"
                "Accept-Language: en-us\n\n"
                "licenseID=string&content=string&/paramsXML=string")

request = HttpRequest(POST_request)
