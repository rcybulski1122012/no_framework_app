from pathlib import Path

import app.auth.models
import app.core.http.sessions
import app.todolists.models

APP_DIR = Path(__file__).parent.absolute()
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

psql_extensions = ["uuid-ossp"]

models_modules = [
    app.auth.models,
    app.core.http.sessions,
    app.todolists.models,
]

ACCEPTED_STATIC_MIME_TYPES = {"css": "text/css", "js": "text/javascript"}
