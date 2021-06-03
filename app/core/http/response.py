from dataclasses import dataclass


@dataclass
class HttpResponse:
    version: str
    status_code: int
    readable: str
    headers: dict = None
    body: str = ""

    def __str__(self):
        response = f"{self.version} {self.status_code} {self.readable}\n"
        if self.headers:
            response += self._format_headers(self.headers)
        if self.body:
            response += f"\n{self.body}\n"
        return response

    def get_response(self):
        return str(self).encode("utf-8")

    @staticmethod
    def _format_headers(headers):
        result = ""
        for header, value in headers.items():
            result += f"{header}: {value}\n"
        return result
