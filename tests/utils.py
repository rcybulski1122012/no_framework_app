import json

from app.core.http.request import HttpRequest


def create_request(method, path, version, session=None, body=None):
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

    return HttpRequest(raw_request.encode())
