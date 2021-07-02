from pathlib import Path

import pytest

from app.core.shortcuts import json_response, render_static, render_template


def test_render_template(tmpdir, GET_request_obj):
    p = tmpdir.mkdir("files").join("file.html")
    p.write("content")
    response_body = render_template(
        GET_request_obj, "file.html", templates_dir=Path(p.dirpath())
    ).body
    assert response_body == "content"


@pytest.mark.parametrize(
    "variable_format",
    [
        "{{var}}",
        "{{ var }}",
        "{{var }}",
        "{{ var}}",
        "{{      var       }}",
        "{{\t\t \t \n var \t }}",
    ],
)
def test_render_template_replaces_variables(tmpdir, variable_format, GET_request_obj):
    p = tmpdir.mkdir("files").join("file.html")
    p.write(f"content {variable_format}")

    response_body = render_template(
        GET_request_obj, "file.html", templates_dir=Path(p.dirpath()), var="Variable"
    ).body
    assert response_body == "content Variable"


def test_json_response(GET_request_obj):
    expected = '{"test": 2, "values": ["t", "e", "s", "t"]}'
    response_body = json_response(
        GET_request_obj, {"test": 2, "values": ["t", "e", "s", "t"]}
    ).body

    assert response_body == expected


def test_render_static(tmpdir, GET_request_obj):
    p = tmpdir.mkdir("files").join("file.css")
    p.write("h2{color:red;}")

    response = render_static(
        GET_request_obj,
        MIME_type="text/css",
        path="file.css",
        static_dir=Path(p.dirpath()),
    )

    assert response.body == "h2{color:red;}"
    assert response.headers["Content-Type"] == "text/css"
