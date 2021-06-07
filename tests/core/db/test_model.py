import pytest

from app.core.db.model import Field, Model
from app.core.errors import MissingRequiredArgument


def test_field_dunder_set_name_sets_name(field, dummy_class):
    field.__set_name__(dummy_class, "field")

    assert field.column_name == "field"


def test_field_dunder_set_name_add_field_to_fields_list_if_exists():
    first = Field("integer")
    second = Field("integer")

    class Mock:
        _fields = [first]

    second.__set_name__(Mock, "second")

    assert Mock._fields == [first, second]


def test_field_dunder_set_name_creates_fields_attribute_in_owner_if_does_not_exist(
    field, dummy_class
):
    field.__set_name__(dummy_class, "field")

    assert dummy_class._fields == [field]


def test_field_dunder_get_returns_field_if_instance_is_None(field):
    result = field.__get__(None, None)

    assert result == field


def test_field_dunder_get_returns_field_value_if_instance_is_not_None(
    field, dummy_class
):
    instance = dummy_class()
    field._values[instance] = expected = 5
    result = field.__get__(instance, None)

    assert result == expected


def test_field_dunder_set(field, dummy_class):
    instance = dummy_class()
    field.__set__(instance, 5)

    assert field._values[instance] == 5


def test_model_init_raises_exception_when_argument_not_provided(model):
    with pytest.raises(MissingRequiredArgument):
        model(first=5)


def test_model_init_does_not_require_argument_when_default_is_provided():
    class Class(Model):
        field = Field("integer", default=5)

    instance = Class()

    assert instance.field == 5


def test_model_dunder_init_subclass_copies_fields_attr_and_removes_foreign_fields(
    model,
):
    expected_TestModel = ["id_", "first", "second", "third"]
    expected_Model = ["id_"]

    assert model._fields is not Model._fields
    assert model.get_fields_names() == expected_TestModel
    assert Model.get_fields_names() == expected_Model


def test_model_init_properly_assigns_value_to_field():
    class Class(Model):
        field = Field("integer")

    instance = Class(field=5)

    assert instance.field == 5


def test_model_get_table_name(model):
    result = model.get_table_name()
    expected = "testmodel"
    assert result == expected


def test_model_get_fields_names(model):
    result = model.get_fields_names()
    expected = ["id_", "first", "second", "third"]

    assert result == expected


def test_model_get_field_values_dict(model):
    instance = model(first=1, second=2, third=3)
    result = instance.get_fields_values_dict()
    expected = {"id_": None, "first": 1, "second": 2, "third": 3}

    assert result == expected


def test_model_from_query_response(model):
    args = [1, 2, 3, 4]
    instance = model.create_from_query_response(args)

    assert instance.id_ == 1
    assert instance.first == 2
    assert instance.second == 3
    assert instance.third == 4
