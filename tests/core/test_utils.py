from unittest.mock import Mock

import pytest

from app.core.errors import Http400
from app.core.utils import CaseInsensitiveDict, get_data_from_request_body


def test_case_insensitive_dict():
    d = CaseInsensitiveDict()
    d["TeSt"] = 5

    assert d["test"] == d["TeSt"] == d["tEsT"]


def test_get_data_from_request_body_raises_400_when_invalid_format():
    request = Mock()
    request.body = "{'invalid': ,json data;}"

    with pytest.raises(Http400):
        get_data_from_request_body(request, ["test"])


def test_get_data_from_request_body_raises_400_when_lack_of_required_field():
    request = Mock()
    request.body = '{"first": 1, "second": 2}'

    with pytest.raises(Http400):
        get_data_from_request_body(request, ["third", "fourth"])


def test_get_data_from_request_body_returns_required_fields():
    request = Mock()
    request.body = '{"first": 1, "second": 2, "third": 3}'
    expected = [1, 2, 3]
    result = get_data_from_request_body(request, ["first", "second", "third"])

    assert result == expected
