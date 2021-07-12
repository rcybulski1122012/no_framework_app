from app.auth.models import AppUser
from app.core.db.model import Field, Model
from app.core.db.validators import MaxLenValidator, MinLenValidator


class ToDoList(Model):
    name = Field("varchar(64)", validators=[MinLenValidator(1), MaxLenValidator(64)])
    description = Field("varchar(256)", default="''", validators=[MaxLenValidator(256)])
    creator_id = Field("integer")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._creator = None
        self._tasks = None

    @property
    def creator(self):
        if self._creator is None:
            try:
                self._creator = AppUser.select(id_=self.creator_id)[0]
            except IndexError:
                return None
        return self._creator

    @property
    def tasks(self):
        if self._tasks is None:
            self._tasks = Task.select(todolist_id=self.id_)
        return self._tasks


class Task(Model):
    content = Field(
        "varchar(128)", validators=[MinLenValidator(1), MaxLenValidator(128)]
    )
    is_done = Field("boolean", default=False)
    todolist_id = Field("integer")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._todolist = None

    @property
    def todolist(self):
        if self._todolist is None:
            try:
                self._todolist = ToDoList.select(id_=self.todolist_id)[0]
            except IndexError:
                return None

        return self._todolist
