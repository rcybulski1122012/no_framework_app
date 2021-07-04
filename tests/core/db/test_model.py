import pytest

from app.core.db.model import Field, Model
from app.core.errors import MissingRequiredArgument, ModelDeletionException
from tests.core.db.utils import get_all_tables


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


def test_model_init_properly_assigns_value_to_field(instance):
    assert (instance.first, instance.second, instance.third) == (1, 2, 3)


def test_model_dunder_str(instance):
    instance.id_ = 1
    result = str(instance)
    expected = "TestModel(first=1, second=2, third=3)"

    assert result == expected


def test_model_get_table_name(model):
    result = model.get_table_name()
    expected = "testmodel"
    assert result == expected


def test_model_get_fields_names(model):
    result = model.get_fields_names()
    expected = ["id_", "first", "second", "third"]

    assert result == expected


def test_model_get_fields_names_with_exclude(model):
    result = model.get_fields_names(exclude=["id_"])
    expected = ["first", "second", "third"]

    assert result == expected


def test_model_get_field_values_dict(instance):
    result = instance.get_fields_values_dict()
    expected = {"id_": None, "first": 1, "second": 2, "third": 3}

    assert result == expected


def test_model_get_fields_values_dict_with_exclude(instance):
    result = instance.get_fields_values_dict(exclude=["id_"])
    expected = {"first": 1, "second": 2, "third": 3}

    assert result == expected


def test_model_create_from_query_response(model):
    args = [1, 2, 3, 4]
    instance = model.create_from_query_response(args)

    assert instance.id_ == 1
    assert instance.first == 2
    assert instance.second == 3
    assert instance.third == 4


def test_model_create_table(model):
    db_conn = model.db
    before = get_all_tables(db_conn)
    assert "testmodel" not in before

    model.create_table()
    after = get_all_tables(db_conn)

    assert "testmodel" in after


def test_model_save_inserts_new_object_when_id_is_None(instance):
    instance.create_table()
    instance.save()
    result = instance.select()

    assert instance.id_ is not None
    assert result != []


def test_model_save_update_existing_object_when_id_is_not_None(instance):
    instance.create_table()
    instance.save()
    id_ = instance.id_
    instance.first = 11
    instance.save()

    result = instance.select()

    assert instance.id_ == id_
    assert len(result) == 1
    assert result[0].first == 11


def test_model_delete_deletes_object(instance):
    instance.create_table()
    instance.save()

    before = instance.select()
    assert before != []

    instance.delete()
    after = instance.select()

    assert instance.id_ is None
    assert after == []


def test_model_delete_raises_exception_when_model_id_is_none(instance):
    with pytest.raises(ModelDeletionException):
        instance.delete()


def test_model_select_order_by(model):
    model.create_table()
    model.create(first=5, second=2, third=2)
    model.create(first=1, second=2, third=2)
    model.create(first=10, second=2, third=2)

    result = model.select(order_by="first")
    reprs = [str(instance) for instance in result]
    expected = [
        "TestModel(first=1, second=2, third=2)",
        "TestModel(first=5, second=2, third=2)",
        "TestModel(first=10, second=2, third=2)",
    ]

    assert reprs == expected


def test_model_select_desc(model):
    model.create_table()
    model.create(first=5, second=2, third=2)
    model.create(first=1, second=2, third=2)
    model.create(first=10, second=2, third=2)

    result = model.select(order_by="first", asc=False)
    reprs = [str(instance) for instance in result]
    expected = [
        "TestModel(first=10, second=2, third=2)",
        "TestModel(first=5, second=2, third=2)",
        "TestModel(first=1, second=2, third=2)",
    ]

    assert reprs == expected


def test_model_select_limit(model):
    model.create_table()
    model.create(first=5, second=2, third=2)
    model.create(first=1, second=2, third=2)
    model.create(first=10, second=2, third=2)

    result = model.select(limit=1)

    assert len(result) == 1


def test_model_select_conditions(model):
    model.create_table()
    model.create(first=5, second=2, third=2)
    model.create(first=1, second=2, third=2)
    model.create(first=10, second=2, third=2)

    result = model.select(id_=1)

    assert len(result) == 1
    assert result[0].id_ == 1


def test_model_create_saves_object_in_db(model):
    model.create_table()
    instance = model.create(first=1, second=2, third=3)
    result = model.select(id_=instance.id_)

    assert len(result) == 1


def test_model_truncate_table(model):
    model.create_table()
    instance = model.create(first=1, second=2, third=3)
    before = model.select(id_=instance.id_)

    assert len(before) == 1

    model.truncate_table()
    after = model.select(id_=instance.id_)

    assert len(after) == 0
