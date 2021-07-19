from pathlib import Path
from unittest.mock import Mock

import pytest

from app.auth.models import AppUser
from app.core.http.errors import Http400, Http404
from app.core.shortcuts import (
    get_data_from_request_body,
    get_object_or_404,
    json_response,
    render_static,
    render_template,
)


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


def test_get_data_from_request_body_raises_400_when_invalid_format():
    request = Mock()
    request.body = "{'invalid': ,json data;}"

    with pytest.raises(Http400):
        get_data_from_request_body(request, ["test"])


def test_get_data_from_request_body_raises_400_when_lack_of_required_field():
    request = Mock()
    request.body = '{"first": 1, "second": 2}'

    with pytest.raises(Http400):
        get_data_from_request_body(request, ["third", "fourth"])


def test_get_data_from_request_body_returns_required_fields():
    request = Mock()
    request.body = '{"first": 1, "second": 2, "third": 3}'
    expected = [1, 2, 3]
    result = get_data_from_request_body(request, ["first", "second", "third"])

    assert result == expected


def test_get_object_or_404_returns_model_instance(user_and_session):
    user = user_and_session[0]
    result = get_object_or_404(AppUser, id_=user.id_)
    assert str(user) == str(result)


def test_get_object_or_404_raises_404_when_object_does_not_exist():
    with pytest.raises(Http404):
        get_object_or_404(AppUser, id_=100)
