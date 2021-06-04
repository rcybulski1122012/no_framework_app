import pytest

from app.core.db.model import Field
from app.core.db.queries_generator import QueriesGenerator as q


def test_get_field_sql_repr(dummy_class):
    field = Field("integer", nullable=False, default="5", unique=True, primary_key=True)
    field.__set_name__(dummy_class, "field")
    result = q.get_field_sql_repr(field)
    expected = "field integer NOT NULL DEFAULT 5 UNIQUE PRIMARY KEY"

    assert result == expected


def test_get_create_table_query():
    result = q.get_create_table_query(
        "testmodel", ["first_field_repr", "second_fields_repr"]
    )
    expected = (
        "CREATE TABLE IF NOT EXISTS testmodel (first_field_repr, second_fields_repr);"
    )

    assert result == expected


def test_get_insert_query():
    result = q.get_insert_query("testmodel", ["first", "second", "third"])
    expected = "INSERT INTO testmodel (first, second, third) VALUES (%(first)s, %(second)s, %(third)s);"

    assert result == expected


def test_get_insert_query_witH_returning_given():
    result = q.get_insert_query(
        "testmodel", ["first", "second", "third"], returning="id_"
    )
    expected = "INSERT INTO testmodel (first, second, third) VALUES (%(first)s, %(second)s, %(third)s) RETURNING id_;"

    assert result == expected


def test_get_update_query():
    result = q.get_update_query(
        "testmodel", ["first", "second"], ["first_condition", "second_condition"]
    )
    expected = "UPDATE testmodel SET first=%(first)s, second=%(second)s WHERE first_condition AND second_condition;"

    assert result == expected


def test_get_delete_query():
    result = q.get_delete_query("testmodel", ["first_condition", "second_condition"])
    expected = "DELETE FROM testmodel WHERE first_condition AND second_condition;"

    assert result == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"table_name": "testmodel"}, "SELECT * FROM testmodel;"),
        (
            {"table_name": "testmodel", "fields_names": ["first", "second"]},
            "SELECT first, second FROM testmodel;",
        ),
        (
            {"table_name": "testmodel", "conditions": ["first", "second"]},
            "SELECT * FROM testmodel WHERE first AND second;",
        ),
        (
            {"table_name": "testmodel", "order_by": "first"},
            "SELECT * FROM testmodel ORDER BY first ASC;",
        ),
        (
            {"table_name": "testmodel", "order_by": ("first", "second"), "asc": False},
            "SELECT * FROM testmodel ORDER BY first DESC, second DESC;",
        ),
        ({"table_name": "testmodel", "limit": 5}, "SELECT * FROM testmodel LIMIT 5;"),
        (
            {
                "table_name": "testmodel",
                "fields_names": ["first", "second"],
                "conditions": ["condition"],
                "order_by": "first",
                "limit": 1,
            },
            "SELECT first, second FROM testmodel WHERE condition ORDER BY first ASC LIMIT 1;",
        ),
    ],
)
def test_get_select_query(kwargs, expected):
    result = q.get_select_query(**kwargs)

    assert result == expected
