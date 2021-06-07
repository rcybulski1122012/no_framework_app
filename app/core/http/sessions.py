from app.core.db.model import Field, Model
from app.core.db.queries_generator import QueriesGenerator
from app.core.errors import SessionDoesNotExist


class Session(Model):
    session_id = Field("uuid", default="uuid_generate_v4()")
    user_id = Field("integer", nullable=False)
