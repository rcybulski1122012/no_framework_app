import pytest

from app.core.db.model import Field
from app.core.db.queries_generator import QueriesGenerator as q
from app.core.errors import InvalidCondition


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
        "testmodel", ["first", "second"], {"first": 5, "second": 10}
    )
    expected = f"UPDATE testmodel SET first=%(first)s, second=%(second)s WHERE first = %({q.CONDITION_PREFIX}first)s AND second = %({q.CONDITION_PREFIX}second)s;"

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
            {"table_name": "testmodel", "conditions": {"first": 5, "second": 10}},
            f"SELECT * FROM testmodel WHERE first = %({q.CONDITION_PREFIX}first)s AND second = %({q.CONDITION_PREFIX}second)s;",
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
                "conditions": {"condition": 5},
                "order_by": "first",
                "limit": 1,
            },
            f"SELECT first, second FROM testmodel WHERE condition = %({q.CONDITION_PREFIX}condition)s ORDER BY first ASC LIMIT 1;",
        ),
    ],
)
def test_get_select_query(kwargs, expected):
    result = q.get_select_query(**kwargs)

    assert result == expected


def test_format_conditions_placeholders_equal():
    result = q.format_conditions_placeholders({"field": 5})
    expected = [f"field = %({q.CONDITION_PREFIX}field)s"]

    assert result == expected


def test_format_conditions_placeholders_equal_when_condition_has_3_underscores():
    result = q.format_conditions_placeholders({"id___gte": 5})
    expected = [f"id_ >= %({q.CONDITION_PREFIX}id___gte)s"]

    assert result == expected


def test_format_conditions_placeholders_with_multiple_conditions():
    result = q.format_conditions_placeholders({"first": 5, "second__lt": 10})
    expected = [f"first = %({q.CONDITION_PREFIX}first)s", f"second < %({q.CONDITION_PREFIX}second__lt)s"]

    assert result == expected


def test_format_conditions_placeholders_when_operator_is_not_recognized():
    with pytest.raises(InvalidCondition):
        q.format_conditions_placeholders({"field__not-condition": 5})


def test_create_conditions_dict_with_prefixes():
    result = q.create_conditions_dict_with_prefixes({"first": 5, "second": 10, "third": 15})
    expected = {f"{q.CONDITION_PREFIX}first": 5, f"{q.CONDITION_PREFIX}second": 10, f"{q.CONDITION_PREFIX}third": 15}

    assert result == expected
