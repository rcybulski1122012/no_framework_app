import re
from json import dumps

from app.core.http.response import HttpResponse
from app.settings import STATIC_DIR, TEMPLATES_DIR


def json_response(request, response_dict):
    body = dumps(response_dict)
    headers = {"Content-Type": "application/json", "Content-Length": len(body)}
    return HttpResponse(request.version, 200, "OK", headers, body)


def render_template(request, path, *, templates_dir=TEMPLATES_DIR, **kwargs):
    with open(templates_dir / path) as f:
        body = f.read()

    for key, value in kwargs.items():
        pattern = re.compile(r"{{\s*" + key + r"\s*}}")
        matches = pattern.finditer(body)

        for match in matches:
            start, stop = match.span()
            body = body[:start] + value + body[stop:]

    headers = {"Content-Type": "text/html", "Content-Length": len(body)}
    return HttpResponse(request.version, 200, "OK", headers, body)


def render_static(request, MIME_type, path, static_dir=STATIC_DIR):
    with open(static_dir / path) as f:
        body = f.read()

    headers = {"Content-Type": MIME_type, "Content-Length": len(body)}
    return HttpResponse(request.version, 200, "OK", headers, body)
