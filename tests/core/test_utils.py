from app.core.utils import CaseInsensitiveDict, get_models_from_modules
from tests.core import fake_models


def test_case_insensitive_dict():
    d = CaseInsensitiveDict()
    d["TeSt"] = 5

    assert d["test"] == d["TeSt"] == d["tEsT"]


def test_get_models_from_modules():
    result = get_models_from_modules([fake_models])
    expected = [fake_models.First, fake_models.Second, fake_models.Third]

    assert result == expected
