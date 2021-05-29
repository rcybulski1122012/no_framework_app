from pathlib import Path

import pytest

from app.core.shortcuts import render_template, json_response


def test_render_template(tmpdir):
    p = tmpdir.mkdir("files").join("file.html")
    p.write("content")

    assert render_template("file.html", templates_dir=Path(p.dirpath())) == (
        "content",
        "text/html",
    )


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
def test_render_template_replaces_variables(tmpdir, variable_format):
    p = tmpdir.mkdir("files").join("file.html")
    p.write(f"content {variable_format}")

    assert render_template(
        "file.html", templates_dir=Path(p.dirpath()), var="Variable"
    ) == ("content Variable", "text/html")


def test_json_response():
    result = json_response({"test": 2, "values": ["t", "e", "s", "t"]})
    expected = '{"test": 2, "values": ["t", "e", "s", "t"]}', "application/json"
    assert result == expected
