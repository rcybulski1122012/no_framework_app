import pytest

from app.core.errors import Http404


def test_route_without_variables(router, view):
    router.routes = {"/test": view}
    assert router.route("/test") == (view, {})


def test_route_with_variables(router, view):
    router.routes = {"/test/<name>": view}
    assert router.route("/test/bob") == (view, {"name": "bob"})

    router.routes = {"/test/<first>/<second>": view}
    assert (view, {"first": "ooo", "second": "aaa"}) == router.route("/test/ooo/aaa")


def test_route_raises_exception_when_view_is_not_registered(router):
    with pytest.raises(Http404):
        router.route("test_view")


def test_route_returns_404_when_cant_compare_paths(router, monkeypatch):
    def stub(*args, **kwargs):
        raise IndexError

    monkeypatch.setattr(router, "_are_paths_matching", stub)

    with pytest.raises(Http404):
        router.route("test_view")
