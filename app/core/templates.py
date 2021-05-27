from app.settings import TEMPLATES_DIR


def render_template(path, *, templates_dir=TEMPLATES_DIR, **kwargs):
    with open(templates_dir / path) as f:
        template = f.read()

    for key, value in kwargs.items():
        template = template.replace("{{ " + key + " }}", value)

    return template
