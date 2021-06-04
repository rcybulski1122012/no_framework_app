class QueriesGenerator:
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

    @staticmethod
    def get_update_query(table_name, fields_names, conditions):
        formatted_fields = ", ".join([f"{name}=%({name})s" for name in fields_names])
        formatted_conditions = " AND ".join(conditions)
        query = (
            f"UPDATE {table_name} SET {formatted_fields} WHERE {formatted_conditions};"
        )

        return query

    @staticmethod
    def get_delete_query(table_name, conditions):
        formatted_conditions = " AND ".join(conditions)
        query = f"DELETE FROM {table_name} WHERE {formatted_conditions};"

        return query

    @staticmethod
    def get_select_query(
        table_name,
        fields_names=None,
        conditions=None,
        order_by=None,
        asc=True,
        limit=None,
    ):
        formatted_fields_names = ", ".join(fields_names) if fields_names else "*"
        query = f"SELECT {formatted_fields_names} FROM {table_name}"
        if conditions:
            query += " WHERE "
            query += " AND ".join(conditions)

        ordering = "ASC" if asc else "DESC"

        if isinstance(order_by, str):
            query += f" ORDER BY {order_by} {ordering}"
        elif isinstance(order_by, (list, tuple)):
            formatted = ", ".join(map(lambda x: f"{x} {ordering}", order_by))
            query += f" ORDER BY {formatted}"

        if limit:
            query += f" LIMIT {limit}"

        return query + ";"
