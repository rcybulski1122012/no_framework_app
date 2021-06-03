from app.core.db import EQUAL, Field, Model, QueriesGenerator, db
from app.core.errors import SessionDoesNotExist


class Session(Model):
    session_id = Field("uuid", default="uuid_generate_v4()")
    user_id = Field("integer", nullable=False)

    @classmethod
    def get_user_id(cls, session):
        generator = QueriesGenerator(cls)
        query = generator.get_select_query(
            fields_names=["session_id"], conditions=[EQUAL("session_id", session)]
        )
        result = db.execute_query(query)[0]
        if result is None:
            raise SessionDoesNotExist()
        else:
            return int(result)
