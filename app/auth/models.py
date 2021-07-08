import bcrypt

from app.core.db.model import Field, Model
from app.core.db.validators import (AllowedCharsValidator, EmailValidator,
                                    MaxLenValidator, MinLenValidator,
                                    PasswordValidator)


class AppUser(Model):
    username = Field(
        "varchar(32)",
        unique=True,
        validators=[
            MinLenValidator(8),
            MaxLenValidator(32),
            AllowedCharsValidator(),
        ],
    )
    email = Field("varchar(256)", unique=True, validators=[EmailValidator()])
    password = Field("bytea", validators=[PasswordValidator()])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if isinstance(self.password, str):
            bin_passwd = bytes(self.password, "utf-8")
            self.password = bcrypt.hashpw(bin_passwd, bcrypt.gensalt())
        elif isinstance(self.password, memoryview):
            self.password = self.password.tobytes()
