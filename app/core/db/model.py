from weakref import WeakKeyDictionary
from app.core.errors import MissingRequiredArgument, ModelUpdateException, ModelDeletionException


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

        fields = self.fields[1:]    # remove id_
        for field in fields:
            name = field.column_name
            try:
                setattr(self, name, kwargs[name])
            except KeyError:
                if field.default is not None:
                    setattr(self, name, field.default)
                else:
                    raise MissingRequiredArgument(f"Missing required argument: '{name}'")

    def get_fields_values_dict(self):
        fields_names = self.get_fields_names()
        result = {name: getattr(self, name) for name in fields_names}

        return result

    @classmethod
    def get_fields_names(cls):
        names = [field.column_name for field in cls.fields]
        return names

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_create_table_query(cls):
        fields_info = ",".join([field.to_sql() for field in cls.fields])
        query = f"CREATE TABLE IF NOT EXIST {cls.get_table_name()} ({fields_info});"

        return query

    @classmethod
    def get_insert_query(cls, fields_names=None):
        fields_names = fields_names or cls.get_fields_names()[1:]  # all except id_
        formatted_fields_names = ', '.join(fields_names)
        table_name = cls.get_table_name()
        placeholders = ", ".join([f"%({name})s" for name in fields_names])
        query = f"INSERT INTO {table_name} ({formatted_fields_names}) VALUES ({placeholders});"

        return query

    def get_update_query(self, fields_names=None):
        if not self.id_:
            raise ModelUpdateException("You can't update a record which does not exist in database")

        fields_names = fields_names or self.get_fields_names()[1:]
        formatted_fields = ", ".join([f"{name}=%({name})s" for name in fields_names])
        table_name = self.get_table_name()
        query = f"UPDATE {table_name} SET {formatted_fields} WHERE id_={self.id_};"

        return query

    def get_delete_query(self):
        if not self.id_:
            raise ModelDeletionException("You can't delete a record which does not exist in database")

        query = f"DELETE FROM {self.get_table_name()} WHERE id_={self.id_}"

        return query

    @classmethod
    def get_select_query(cls, fields_names=None, *, order_by=None, limit=None, **conditions):
        fields_names = ", ".join(fields_names) if fields_names else "*"
        table_name = cls.get_table_name()
        query = f"SELECT {fields_names} FROM {table_name}"
        if conditions:
            query += " WHERE "
            query += " AND ".join([f"{key}={value}" for key, value in conditions.items()])

        if order_by:
            query += f"ORDER BY {order_by} "

        if limit:
            query += f"LIMIT {limit} "

        return query + ";"


