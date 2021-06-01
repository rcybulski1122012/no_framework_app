import pytest

from app.core.db.model import Field, Model
from app.core.errors import MissingRequiredArgument, ModelUpdateException, ModelDeletionException


@pytest.fixture
def model():
    class TestModel(Model):
        first = Field("integer")
        second = Field("integer")

    return TestModel


@pytest.fixture
def field():
    return Field("integer", nullable=False, default="5", unique=True, primary_key=True)


@pytest.fixture
def dummy_class():
    class Mock:
        pass

    return Mock


def test_field_dunder_set_name_sets_name(field, dummy_class):
    field.__set_name__(dummy_class, "field")

    assert field.column_name == "field"


def test_field_dunder_set_name_add_field_to_fields_list_if_exists():
    first = Field("integer")
    second = Field("integer")

    class Mock:
        fields = [first]

    second.__set_name__(Mock, "second")

    assert Mock.fields == [first, second]


def test_field_dunder_set_name_creates_fields_attribute_in_owner_if_does_not_exist(field, dummy_class):
    field.__set_name__(dummy_class, "field")

    assert dummy_class.fields == [field]


def test_field_dunder_get_returns_field_if_instance_is_None(field):
    result = field.__get__(None, None)

    assert result == field


def test_field_dunder_get_returns_field_value_if_instance_is_not_None(field, dummy_class):
    instance = dummy_class()
    field._values[instance] = expected = 5
    result = field.__get__(instance, None)

    assert result == expected


def test_field_dunder_set(field, dummy_class):
    instance = dummy_class()
    field.__set__(instance, 5)

    assert field._values[instance] == 5


def test_field_to_sql(dummy_class):
    field = Field("integer", nullable=False, default="5", unique=True, primary_key=True)
    field.__set_name__(dummy_class, "field")
    expected = "field integer NOT NULL DEFAULT 5 UNIQUE PRIMARY KEY"

    assert field.to_sql() == expected


def test_model_init_raises_exception_when_argument_not_provided(model):
    with pytest.raises(MissingRequiredArgument):
        model(first=5)


def test_model_get_fields_names():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")

    expected = ["id_", "first", "second"]

    assert Class.get_fields_names() == expected


def test_model_dunder_init_subclass_copies_fields_attr_and_removes_foreign_fields():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")

    expected_Class = ["id_", "first", "second"]
    expected_Model = ["id_"]

    assert Class.fields is not Model.fields
    assert Class.get_fields_names() == expected_Class
    assert Model.get_fields_names() == expected_Model


def test_model_init_does_not_require_argument_when_default_is_provided():
    class Class(Model):
        field = Field("integer", default=5)

    instance = Class()

    assert instance.field == 5


def test_model_init_properly_assigns_value_to_field():
    class Class(Model):
        field = Field("integer")

    instance = Class(field=5)

    assert instance.field == 5


def test_model_get_table_name():
    class Class(Model):
        pass

    assert Class.get_table_name() == "class"


def test_model_get_insert_query_when_fields_are_not_specified():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    result = Class.get_insert_query()
    expected = "INSERT INTO class (first, second, third) VALUES (%(first)s, %(second)s, %(third)s);"

    assert result == expected


def test_model_get_insert_query_when_fields_are_specified():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    result = Class.get_insert_query(["first", "second"])
    expected = "INSERT INTO class (first, second) VALUES (%(first)s, %(second)s);"

    assert result == expected


def test_model_get_field_values_dict():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    instance = Class(first=1, second=2, third=3)
    result = instance.get_fields_values_dict()
    expected = {"id_": None, "first": 1, "second": 2, "third": 3}

    assert result == expected


def test_model_get_update_query_when_fields_are_not_specified():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    instance = Class(first=1, second=2, third=3)
    instance.id_ = 1
    result = instance.get_update_query()
    expected = "UPDATE class SET first=%(first)s, second=%(second)s, third=%(third)s WHERE id_=1;"

    assert result == expected


def test_model_get_update_query_when_fields_are_specified():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    instance = Class(first=1, second=2, third=3)
    instance.id_ = 1
    result = instance.get_update_query(["first", "second"])
    expected = "UPDATE class SET first=%(first)s, second=%(second)s WHERE id_=1;"

    assert result == expected


def test_model_get_update_query_raises_exception_when_model_instance_has_no_id():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    instance = Class(first=1, second=2, third=3)
    with pytest.raises(ModelUpdateException):
        instance.get_update_query()


def test_model_get_delete_query_raises_exception_when_model_instance_has_no_id():
    class Class(Model):
        first = Field("integer")
        second = Field("integer")
        third = Field("integer")

    instance = Class(first=1, second=2, third=3)
    with pytest.raises(ModelDeletionException):
        instance.get_delete_query()
