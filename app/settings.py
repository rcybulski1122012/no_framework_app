from pathlib import Path

APP_DIR = Path(__file__).parent.absolute()
TEMPLATES_DIR = APP_DIR / "templates"
psql_extensions = ["uuid-ossp"]
