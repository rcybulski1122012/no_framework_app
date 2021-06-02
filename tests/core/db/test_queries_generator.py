import pytest

from app.core.db.model import Field
from app.core.errors import ModelDeletionException, ModelUpdateException


def test_get_field_sql_repr(dummy_class, generator_model):
    field = Field("integer", nullable=False, default="5", unique=True, primary_key=True)
    field.__set_name__(dummy_class, "field")
    result = generator_model.get_field_sql_repr(field)
    expected = "field integer NOT NULL DEFAULT 5 UNIQUE PRIMARY KEY"

    assert result == expected


def test_get_create_table_query(generator_model):
    result = generator_model.get_create_table_query()
    expected = (
        "CREATE TABLE IF NOT EXIST testmodel "
        "(id_ serial NOT NULL PRIMARY KEY, "
        "first integer, "
        "second integer, "
        "third integer);"
    )

    assert result == expected


def test_get_insert_query_when_fields_are_not_specified(generator_model):
    result = generator_model.get_insert_query()
    expected = "INSERT INTO testmodel (first, second, third) VALUES (%(first)s, %(second)s, %(third)s);"

    assert result == expected


def test_get_insert_query_when_fields_are_specified(generator_model):
    result = generator_model.get_insert_query(["first", "second"])
    expected = "INSERT INTO testmodel (first, second) VALUES (%(first)s, %(second)s);"

    assert result == expected


def test_get_update_query_when_fields_are_not_specified(generator_instance):
    generator_instance.instance.id_ = 1
    result = generator_instance.get_update_query()
    expected = "UPDATE testmodel SET first=%(first)s, second=%(second)s, third=%(third)s WHERE id_=1;"

    assert result == expected


def test_get_update_query_when_fields_are_specified(generator_instance):
    generator_instance.instance.id_ = 1
    result = generator_instance.get_update_query(["first", "second"])
    expected = "UPDATE testmodel SET first=%(first)s, second=%(second)s WHERE id_=1;"

    assert result == expected


def test_get_update_query_raises_exception_when_model_instance_has_no_id(
    generator_instance,
):
    with pytest.raises(ModelUpdateException):
        generator_instance.get_update_query()


def test_get_delete_query_raises_exception_when_model_instance_has_no_id(
    generator_instance,
):
    with pytest.raises(ModelDeletionException):
        generator_instance.get_delete_query()


@pytest.mark.parametrize("kwargs, expected", [
    ({}, "SELECT * FROM testmodel;"),
    ({"fields_names": ["first", "third"]}, "SELECT first, third FROM testmodel;"),
    ({"order_by": "first"}, "SELECT * FROM testmodel ORDER BY first;"),
    ({"limit": 5}, "SELECT * FROM testmodel LIMIT 5;"),
    ({"conditions": ["first=5", "second IN (2,3,4)"]}, "SELECT * FROM testmodel WHERE first=5 AND second IN (2,3,4);"),
    ({"fields_names": ["first"], "order_by": "first", "limit": 2, "conditions": ["second < first"]},
     "SELECT first FROM testmodel WHERE second < first ORDER BY first LIMIT 2;")
])
def test_select_query(generator_model, kwargs, expected):
    result = generator_model.get_select_query(**kwargs)

    assert result == expected
