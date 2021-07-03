from app.core.errors import InvalidCondition


class QueriesGenerator:
    OPERATORS = {
        "gt": ">",
        "gte": ">=",
        "lt": "<",
        "lte": ">",
        "neq": "<>",
        "like": "LIKE",
    }
    CONDITION_PREFIX = "c_"

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

    @staticmethod
    def get_create_table_query(table_name, fields_repr):
        formatted_fields = ", ".join(fields_repr)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({formatted_fields});"

        return query

    @staticmethod
    def get_insert_query(table_name, fields_names, *, returning=None):
        formatted_fields_names = ", ".join(fields_names)
        placeholders = ", ".join([f"%({name})s" for name in fields_names])
        query = f"INSERT INTO {table_name} ({formatted_fields_names}) VALUES ({placeholders})"

        if returning:
            query += f" RETURNING {returning};"
        else:
            query += ";"

        return query

    @classmethod
    def get_update_query(cls, table_name, fields_names, conditions):
        formatted_fields = ", ".join([f"{name}=%({name})s" for name in fields_names])
        formatted_conditions = " AND ".join(
            cls.format_conditions_placeholders(conditions)
        )
        query = (
            f"UPDATE {table_name} SET {formatted_fields} WHERE {formatted_conditions};"
        )

        return query

    @classmethod
    def get_delete_query(cls, table_name, conditions):
        formatted_conditions = " AND ".join(
            cls.format_conditions_placeholders(conditions)
        )
        query = f"DELETE FROM {table_name} WHERE {formatted_conditions};"

        return query

    @classmethod
    def get_select_query(
        cls,
        table_name,
        fields_names=None,
        order_by=None,
        asc=True,
        limit=None,
        conditions=None,
    ):
        formatted_fields_names = ", ".join(fields_names) if fields_names else "*"
        query = f"SELECT {formatted_fields_names} FROM {table_name}"
        if conditions:
            query += " WHERE "
            query += " AND ".join(cls.format_conditions_placeholders(conditions))

        ordering = "ASC" if asc else "DESC"

        if isinstance(order_by, str):
            query += f" ORDER BY {order_by} {ordering}"
        elif isinstance(order_by, (list, tuple)):
            formatted = ", ".join(map(lambda x: f"{x} {ordering}", order_by))
            query += f" ORDER BY {formatted}"

        if limit:
            query += f" LIMIT {limit}"

        return query + ";"

    @classmethod
    def format_conditions_placeholders(cls, conditions):
        """
        Returns list of strings, that are formatted conditions with placeholders.
        Placeholders names are prefixed with cls.CONDITION_PREFIX to avoid errors, so you have
        to adjust your data dict when you pass it to db connection.
        """
        result = []
        keys = conditions.keys()

        for key in keys:
            try:
                # That solves the problem when field name is ended with _
                # e.g. the result of splitting "id___gte" will be ["id", "_gte"]
                # instead of ["id_", "gte"] which would cause a problem
                reversed_key = key[::-1]
                operator, field_name = reversed_key.split("__", 1)
                field_name, operator = field_name[::-1], operator[::-1]
                operator = cls.OPERATORS[operator]
                result.append(
                    f"{field_name} {operator} %({cls.CONDITION_PREFIX}{key})s"
                )
            except ValueError:
                result.append(f"{key} = %({cls.CONDITION_PREFIX}{key})s")
            except KeyError:
                raise InvalidCondition(f"Condition {key} is not recognized")

        return result

    @classmethod
    def create_conditions_dict_with_prefixes(cls, conditions):
        result = {}
        for key, value in conditions.items():
            prefixed_key = f"{cls.CONDITION_PREFIX}{key}"
            result[prefixed_key] = value

        return result

    @classmethod
    def get_truncate_table_query(cls, table_name):
        return f"TRUNCATE {table_name};"
