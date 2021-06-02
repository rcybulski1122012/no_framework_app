from app.core.db.model import Model
from app.core.errors import (InstanceNotProvided, ModelDeletionException,
                             ModelUpdateException)


class QueriesGenerator:
    def __init__(self, model_or_instance):
        if isinstance(model_or_instance, Model):
            self.instance = model_or_instance
            self.model = model_or_instance.__class__
        else:
            self.instance = None
            self.model = model_or_instance

    @staticmethod
    def get_field_sql_repr(field):
        result = f"{field.column_name} {field.data_type}"

        if not field.nullable:
            result += " NOT NULL"
        if field.default is not None:
            result += f" DEFAULT {field.default}"
        if field.unique:
            result += " UNIQUE"
        if field.primary_key:
            result += " PRIMARY KEY"

        return result

    def get_create_table_query(self):
        formatted_fields = ", ".join(
            [self.get_field_sql_repr(field) for field in self.model.fields]
        )
        table_name = self.model.get_table_name()
        query = f"CREATE TABLE IF NOT EXIST {table_name} ({formatted_fields});"

        return query

    def get_insert_query(self, fields_names=None):
        fields_names = (
            fields_names or self.model.get_fields_names()[1:]
        )  # all except id_
        formatted_fields_names = ", ".join(fields_names)
        table_name = self.model.get_table_name()
        placeholders = ", ".join([f"%({name})s" for name in fields_names])
        query = f"INSERT INTO {table_name} ({formatted_fields_names}) VALUES ({placeholders});"

        return query

    def get_update_query(self, fields_names=None):
        if self.instance is None:
            raise InstanceNotProvided("Instance not provided")

        if not self.instance.id_:
            raise ModelUpdateException(
                "You can't update a record which does not exist in database"
            )

        fields_names = fields_names or self.model.get_fields_names()[1:]
        formatted_fields = ", ".join([f"{name}=%({name})s" for name in fields_names])
        table_name = self.model.get_table_name()
        query = (
            f"UPDATE {table_name} SET {formatted_fields} WHERE id_={self.instance.id_};"
        )

        return query

    def get_delete_query(self):
        if self.instance is None:
            raise InstanceNotProvided("Instance not provided")

        if not self.instance.id_:
            raise ModelDeletionException(
                "You can't delete a record which does not exist in database"
            )

        table_name = self.model.get_table_name()
        query = f"DELETE FROM {table_name} WHERE id_={self.instance.id_}"

        return query

    def get_select_query(
        self, fields_names=None, conditions=None, order_by=None, limit=None
    ):
        fields_names = ", ".join(fields_names) if fields_names else "*"
        table_name = self.model.get_table_name()
        query = f"SELECT {fields_names} FROM {table_name}"
        if conditions:
            query += " WHERE "
            query += " AND ".join(conditions)

        if order_by:
            query += f" ORDER BY {order_by}"

        if limit:
            query += f" LIMIT {limit}"

        return query + ";"
