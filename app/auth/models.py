import bcrypt

from app.core.db.model import Model, Field


class AppUser(Model):
    username = Field("varchar(32)", unique=True)
    email = Field("varchar(256)", unique=True)
    password = Field("bytea")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if isinstance(self.password, str):
            bin_passwd = bytes(self.password, "utf-8")
            self.password = bcrypt.hashpw(bin_passwd, bcrypt.gensalt())
        elif isinstance(self.password, memoryview):
            self.password = self.password.tobytes()
