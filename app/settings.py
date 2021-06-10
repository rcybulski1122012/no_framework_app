from pathlib import Path

import app.models

APP_DIR = Path(__file__).parent.absolute()
TEMPLATES_DIR = APP_DIR / "templates"
psql_extensions = ["uuid-ossp"]

models_modules = [app.models]
