from pathlib import Path
from app.core.templates import render_template


def test_render_template(tmpdir):
    p = tmpdir.mkdir("files").join("file.html")
    p.write("content")

    assert render_template("file.html", templates_dir=Path(p.dirpath())) == "content"


def test_render_template_replaces_variables(tmpdir):
    p = tmpdir.mkdir("files").join("file.html")
    p.write("content {{ title }}, {{ author }}")

    assert render_template("file.html", templates_dir=Path(p.dirpath()),
                           title="Title", author="Author") == "content Title, Author"
