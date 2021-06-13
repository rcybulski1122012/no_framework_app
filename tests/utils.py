import json

from app.core.http.request import HttpRequest


def json_request(method, path, body):
    body = json.dumps(body)
    body_len = len(body)

    request = (
        f"{method} {path} HTTP/1.1\n"
        f"Content-Type: application/json"
        f"Content-Length: {body_len}\n\n"
        f"{body}"
    )

    b_request = bytes(request, "utf-8")

    return HttpRequest(b_request)
