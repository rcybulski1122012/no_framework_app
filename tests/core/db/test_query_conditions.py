from app.core.db.query_conditions import *


def test_AND():
    assert AND("first", "second") == "(first AND second)"


def test_OR():
    assert OR("first", "second") == "(first OR second)"


def test_EQUAL():
    assert EQUAL("field", "value") == "field = value"


def test_LESS():
    assert LESS("field", "value") == "field < value"


def test_LESS_OR_EQUAL():
    assert LESS_OR_EQUAL("field", "value") == "field <= value"


def test_GREATER():
    assert GREATER("field", "value") == "field > value"


def test_GREATER_OR_EQUAL():
    assert GREATER_OR_EQUAL("field", "value") == "field >= value"


def test_IS_NULL():
    assert IS_NULL("field") == "field IS NULL"


def test_LIKE():
    assert LIKE("field", "pattern") == "field LIKE 'pattern'"


def test_IN_when_query_given():
    assert IN("field", "SELECT * FROM table") == "field IN (SELECT * FROM table)"


def test_IN_when_values_given():
    assert IN("field", [1, 2, 3]) == "field IN (1, 2, 3)"