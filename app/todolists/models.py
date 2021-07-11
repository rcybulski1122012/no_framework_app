from app.auth.models import AppUser
from app.core.db.model import Field, Model
from app.core.db.validators import MaxLenValidator, MinLenValidator


class ToDoList(Model):
    name = Field("varchar(64)", validators=[MinLenValidator(1), MaxLenValidator(64)])
    description = Field("varchar(256)", default="''", validators=[MaxLenValidator(256)])
    creator_id = Field("integer")

    @property
    def creator(self):
        try:
            return AppUser.select(id_=self.creator_id)[0]
        except IndexError:
            return None

    @property
    def tasks(self):
        return Task.select(todolist_id=self.id_)


class Task(Model):
    content = Field(
        "varchar(128)", validators=[MinLenValidator(1), MaxLenValidator(128)]
    )
    is_done = Field("boolean", default=False)
    todolist_id = Field("integer")

    @property
    def todolist(self):
        try:
            return ToDoList.select(id_=self.todolist_id)[0]
        except IndexError:
            return None
