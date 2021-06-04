from app.core.db.model import Field, Model
from app.core.db.queries import get_select_query
from app.core.db.query_conditions import EQUAL
from app.core.errors import SessionDoesNotExist


class Session(Model):
    session_id = Field("uuid", default="uuid_generate_v4()")
    user_id = Field("integer", nullable=False)

    @classmethod
    def get_user_id(cls, session):
        query = get_select_query(
            cls.get_table_name(), fields_names=["session_id"], conditions=[EQUAL("session_id", session)]
        )
        result = cls._db.execute_query(query)[0]
        if result is None:
            raise SessionDoesNotExist()
        else:
            return int(result)
