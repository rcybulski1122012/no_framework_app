from weakref import WeakKeyDictionary

from app.core.db.db_connection import db
from app.core.db.queries_generator import QueriesGenerator
from app.core.db.query_conditions import EQUAL
from app.core.errors import (MissingRequiredArgument, ModelDeletionException,
                             ModelUpdateException)


class Field:
    def __init__(
        self, data_type, nullable=False, default=None, unique=False, primary_key=False
    ):
        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.primary_key = primary_key

        self._values = WeakKeyDictionary()

    def __set_name__(self, owner, name):
        try:
            owner._fields.append(self)
        except AttributeError:
            owner._fields = [self]

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
    db = db
    queries_generator = QueriesGenerator

    id_ = Field("serial", nullable=False, primary_key=True)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls._fields = cls.__base__._fields.copy()

        for key, value in cls.__dict__.items():
            if isinstance(value, Field):
                cls.__base__._fields.remove(value)

    def __init__(self, **kwargs):
        self.id_ = None

        fields = self._fields[1:]  # remove id_
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
    def from_query_response(cls, args):
        fields_names = cls.get_fields_names()
        kwargs = dict(zip(fields_names, args))
        instance = cls(**kwargs)
        instance.id_ = args[0]
        return instance

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_fields_names(cls):
        names = [field.column_name for field in cls._fields]
        return names

    def get_fields_values_dict(self):
        fields_names = self.get_fields_names()
        result = {name: getattr(self, name) for name in fields_names}

        return result

    def save(self):
        if self.id_ is None:
            self._insert_new_object()
        else:
            self.update()

    def _insert_new_object(self):
        table_name = self.get_table_name()
        fields_names = self.get_fields_names()
        fields_names.remove("id_")
        query = self.queries_generator.get_insert_query(
            table_name, fields_names, returning="id_"
        )
        data = self.get_fields_values_dict()
        self.id_ = db.execute_query(query, data)[0][0]

    def update(self):
        if self.id_ is None:
            raise ModelUpdateException(
                "You can't update an object which hasn't been saved in database"
            )

        table_name = self.get_table_name()
        fields_names = self.get_fields_names()
        fields_names.remove("id_")
        query = self.queries_generator.get_update_query(
            table_name, fields_names, conditions=[EQUAL("id_", self.id_)]
        )
        data = self.get_fields_values_dict()

        self.db.execute_query(query, data)

    def delete(self):
        if self.id_ is None:
            raise ModelDeletionException(
                "You can't delete an object which hasn't been saved in database"
            )

        table_name = self.get_table_name()
        fields_names = self.get_fields_names()
        fields_names.remove("id_")
        query = self.queries_generator.get_delete_query(
            table_name, conditions=[EQUAL("id_", self.id_)]
        )
        self.db.execute_query(query)
        self.id_ = None
