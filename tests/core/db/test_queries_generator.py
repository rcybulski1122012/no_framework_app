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


def test_model_get_delete_query_raises_exception_when_model_instance_has_no_id(
    generator_instance,
):
    with pytest.raises(ModelDeletionException):
        generator_instance.get_delete_query()
