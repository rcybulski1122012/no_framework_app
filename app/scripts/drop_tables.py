from app.core.db.db_connection import db

query = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
db.execute_query(query)
