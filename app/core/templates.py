import re
from app.settings import TEMPLATES_DIR


def render_template(path, *, templates_dir=TEMPLATES_DIR, **kwargs):
    with open(templates_dir / path) as f:
        template = f.read()

    for key, value in kwargs.items():
        pattern = re.compile(r"\{\{\s*" + key + r"\s*\}\}")
        matches = pattern.finditer(template)

        for match in matches:
            start, stop = match.span()
            template = template[:start] + value + template[stop:]

    return template, "text/html"
