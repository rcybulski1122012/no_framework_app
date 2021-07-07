import json
import re

from app.core.errors import Http400, Http404
from app.core.http.response import HttpResponse
from app.settings import STATIC_DIR, TEMPLATES_DIR


def json_response(request, response_dict, *, status_code=200, readable="OK"):
    body = json.dumps(response_dict)
    headers = {"Content-Type": "application/json", "Content-Length": len(body)}
    return HttpResponse(request.version, status_code, readable, headers, body)


def render_template(request, path, *, templates_dir=TEMPLATES_DIR, **kwargs):
    with open(templates_dir / path) as f:
        body = f.read()

    for key, value in kwargs.items():
        pattern = re.compile(r"{{\s*" + key + r"\s*}}")
        matches = pattern.finditer(body)

        for match in matches:
            start, stop = match.span()
            body = body[:start] + str(value) + body[stop:]

    headers = {"Content-Type": "text/html", "Content-Length": len(body)}
    return HttpResponse(request.version, 200, "OK", headers, body)


def render_static(request, MIME_type, path, static_dir=STATIC_DIR):
    with open(static_dir / path) as f:
        body = f.read()

    headers = {"Content-Type": MIME_type, "Content-Length": len(body)}
    return HttpResponse(request.version, 200, "OK", headers, body)


def redirect(request, path):
    headers = {
        "Location": path,
    }
    return HttpResponse(request.version, 302, "Found", headers)


def get_data_from_request_body(request, fields_names):
    try:
        data = json.loads(request.body)
        result = [data[field_name] for field_name in fields_names]
    except (json.decoder.JSONDecodeError, KeyError):
        raise Http400
    else:
        return result


def get_object_or_404(model, **conditions):
    try:
        return model.select(**conditions)[0]
    except IndexError:
        raise Http404
