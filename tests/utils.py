import json

from app.core.http.request import HttpRequest


def json_request(method, path, body, session=None):
    body = json.dumps(body)
    body_len = len(body)

    cookie_str = f"Cookie: session_id={session.session_id}\n\n" if session else "\n"

    request = (
        f"{method} {path} HTTP/1.1\n"
        f"Content-Type: application/json"
        f"Content-Length: {body_len}\n"
        f"{cookie_str}"
        f"{body}"
    )

    print(request)

    b_request = bytes(request, "utf-8")

    return HttpRequest(b_request)
