from unittest.mock import Mock

import pytest

from app.core.errors import Http400
from app.core.shortcuts import get_data_from_request_body
from app.core.utils import CaseInsensitiveDict


def test_case_insensitive_dict():
    d = CaseInsensitiveDict()
    d["TeSt"] = 5

    assert d["test"] == d["TeSt"] == d["tEsT"]
