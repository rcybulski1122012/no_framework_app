def get_all_tables(db_conn):
    query = (
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )
    result = db_conn.execute_query(query)

    return [item[0] for item in result]
