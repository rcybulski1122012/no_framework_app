from weakref import WeakKeyDictionary

from app.core.db.db_connection import db
from app.core.db.queries_generator import QueriesGenerator
from app.core.errors import MissingRequiredArgument, ModelDeletionException


class Field:
    def __init__(
        self,
        data_type,
        nullable=False,
        default=None,
        unique=False,
        primary_key=False,
        validators=None,
    ):
        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.primary_key = primary_key
        self.validators = validators or []

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
        for validator in self.validators:
            validator.validate(value)

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
                elif field.nullable is True:
                    setattr(self, name, None)
                else:
                    raise MissingRequiredArgument(
                        f"Missing required argument: '{name}'"
                    )

    def __repr__(self):
        name = self.__class__.__name__
        fields_names = self.get_fields_names(exclude=("id_",))
        fields_repr = [f"{name}={getattr(self, name)}" for name in fields_names]
        joined_fields_repr = ", ".join(fields_repr)
        return f"{name}({joined_fields_repr})"

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()

        return instance

    @classmethod
    def create_from_query_response(cls, args):
        fields_names = cls.get_fields_names()
        kwargs = dict(zip(fields_names, args))
        instance = cls(**kwargs)
        instance.id_ = args[0]
        return instance

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_fields_names(cls, exclude=tuple()):
        names = [
            field.column_name
            for field in cls._fields
            if field.column_name not in exclude
        ]
        return names

    def get_fields_values_dict(self, exclude=tuple()):
        fields_names = self.get_fields_names(exclude=exclude)
        result = {name: getattr(self, name) for name in fields_names}

        return result

    @classmethod
    def create_table(cls):
        table_name = cls.get_table_name()
        fields_repr = [
            cls.queries_generator.get_field_sql_repr(field) for field in cls._fields
        ]
        query = cls.queries_generator.get_create_table_query(table_name, fields_repr)
        cls.db.execute_query(query)

    @classmethod
    def truncate_table(cls):
        table_name = cls.get_table_name()
        query = cls.queries_generator.get_truncate_table_query(table_name)
        cls.db.execute_query(query)

    def save(self):
        if self.id_ is None:
            self._insert_new_object()
        else:
            self._update()

    def _insert_new_object(self):
        table_name = self.get_table_name()
        fields_names = self.get_fields_names(exclude=("id_",))
        query = self.queries_generator.get_insert_query(
            table_name, fields_names, returning="id_"
        )
        data = self.get_fields_values_dict()
        self.id_ = self.db.execute_query(query, data)[0][0]

    def _update(self):
        table_name = self.get_table_name()
        fields_names = self.get_fields_names(exclude=("id_",))
        conditions = {"id_": self.id_}
        query = self.queries_generator.get_update_query(
            table_name, fields_names, conditions=conditions
        )
        data = self.get_fields_values_dict()
        conditions = self.queries_generator.create_conditions_dict_with_prefixes(
            conditions
        )
        data.update(conditions)

        self.db.execute_query(query, data=data)

    def delete(self):
        if self.id_ is None:
            raise ModelDeletionException(
                "You can't delete an object which hasn't been saved in database"
            )

        table_name = self.get_table_name()
        conditions = {"id_": self.id_}
        query = self.queries_generator.get_delete_query(
            table_name, conditions=conditions
        )
        conditions = self.queries_generator.create_conditions_dict_with_prefixes(
            conditions
        )
        self.db.execute_query(query, data=conditions)
        self.id_ = None

    @classmethod
    def select(cls, order_by=None, asc=True, limit=None, **conditions):
        """
        Conditions work similar to django but they are limited.
        Available conditions:
            "gt": ">",
            "gte": ">=",
            "lt": "<",
            "lte": ">",
            "neq": "<>",
            "like": "LIKE"
        """
        table_name = cls.get_table_name()
        query = cls.queries_generator.get_select_query(
            table_name=table_name,
            fields_names=None,
            order_by=order_by,
            asc=asc,
            limit=limit,
            conditions=conditions,
        )

        prefixed_conditions = (
            cls.queries_generator.create_conditions_dict_with_prefixes(conditions)
        )
        records = cls.db.execute_query(query, data=prefixed_conditions)
        result = [cls.create_from_query_response(record) for record in records]

        return result
