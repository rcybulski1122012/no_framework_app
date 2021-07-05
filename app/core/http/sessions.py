import json
import uuid

from app.core.db.model import Field, Model
from app.core.errors import Http403, InvalidSessionData


class Session(Model):
    session_id = Field("uuid", default="uuid_generate_v4()")
    data = Field("varchar(512)")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            self.json_data = json.loads(self.data)
        except (json.decoder.JSONDecodeError, TypeError):
            if not isinstance(self.data, dict):
                raise InvalidSessionData(
                    "Value of field 'data' must be a dictionary instance"
                    " or string, which can be converted into a dict"
                )
            else:
                self.json_data = self.data
        else:
            if not isinstance(self.json_data, dict):
                raise InvalidSessionData(
                    "Value of field 'data' must be a dictionary instance"
                    " or string, which can be converted into a dict"
                )

        if self.session_id == "uuid_generate_v4()":
            self.session_id = uuid.uuid4()

    def __getitem__(self, key):
        return self.json_data[key]

    def __setitem__(self, key, value):
        self.json_data[key] = value

    def save(self):
        self.data = json.dumps(self.json_data)
        super().save()


def get_current_session_or_403(request):
    try:
        session_id = request.cookies["session_id"]
        session = Session.select(session_id=session_id)[0]
        return session
    except (KeyError, IndexError):
        raise Http403
