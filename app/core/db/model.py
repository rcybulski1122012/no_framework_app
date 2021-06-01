from weakref import WeakKeyDictionary
from app.core.errors import MissingRequiredArgument


class Field:
    def __init__(self, data_type, nullable=True,
                 default=None, unique=False, primary_key=False):
        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.primary_key = primary_key

        self._values = WeakKeyDictionary()

    def __set_name__(self, owner, name):
        try:
            owner.fields.append(self)
        except AttributeError:
            owner.fields = [self]

        self.column_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)

    def __set__(self, instance, value):
        self._values[instance] = value

    def to_sql(self):
        result = f"{self.column_name} {self.data_type}"

        if not self.nullable:
            result += " NOT NULL"
        if self.default is not None:
            result += f" DEFAULT {self.default}"
        if self.unique:
            result += " UNIQUE"
        if self.primary_key:
            result += " PRIMARY KEY"

        return result

    def __repr__(self):
        return f"Field(name={self.column_name})"


class Model:
    id_ = Field("serial", nullable=False, primary_key=True)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.fields = cls.__base__.fields.copy()

        for key, value in cls.__dict__.items():
            if isinstance(value, Field):
                cls.__base__.fields.remove(value)

    def __init__(self, **kwargs):
        self.id_ = None

        fields = self.fields[1:]
        for field in fields:
            name = field.column_name
            try:
                setattr(self, name, kwargs[name])
            except KeyError:
                if field.default is not None:
                    setattr(self, name, field.default)
                else:
                    raise MissingRequiredArgument(f"Missing required argument: '{name}'")

    @classmethod
    def get_create_table_query(cls):
        fields_info = ""
        for field in cls.fields:
            fields_info += f"{field.to_sql()},"

        fields_info = fields_info[:-1]  # remove colon at the end

        query = f"CREATE TABLE IF NOT EXIST {cls.__name__} ({fields_info});"

        return query
