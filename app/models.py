from app.core.db.model import Field, Model


class ToDoList(Model):
    title = Field("varchar(50)")
    user_id = Field("integer")
    description = Field("varchar(200)", default="''")
