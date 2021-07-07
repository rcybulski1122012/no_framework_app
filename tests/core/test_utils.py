from app.core.utils import CaseInsensitiveDict


def test_case_insensitive_dict():
    d = CaseInsensitiveDict()
    d["TeSt"] = 5

    assert d["test"] == d["TeSt"] == d["tEsT"]
