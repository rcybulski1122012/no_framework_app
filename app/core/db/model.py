from weakref import WeakKeyDictionary

from app.core.errors import MissingRequiredArgument


class Field:
    def __init__(
        self, data_type, nullable=True, default=None, unique=False, primary_key=False
    ):
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

        fields = self.fields[1:]  # remove id_
        for field in fields:
            name = field.column_name
            try:
                setattr(self, name, kwargs[name])
            except KeyError:
                if field.default is not None:
                    setattr(self, name, field.default)
                else:
                    raise MissingRequiredArgument(
                        f"Missing required argument: '{name}'"
                    )

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_fields_names(cls):
        names = [field.column_name for field in cls.fields]
        return names

    def get_fields_values_dict(self):
        fields_names = self.get_fields_names()
        result = {name: getattr(self, name) for name in fields_names}

        return result
