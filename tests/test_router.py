import pytest

from app.core.errors import Http404


def test_route_without_variables(router, view):
    router.routes = {"/test": view}
    assert view, {} == router.route("/test")


def test_route_with_variables(router, view):
    router.routes = {"/test/<name>": view}
    assert view, {"name": "bob"} == router.route("/test/bob")

    router.routes = {"test/<first>/<second>": view}
    assert view, {"first": "ooo", "second": "aaa"} == router.route("/test/ooo/aaa")


def test_route_raises_exception_when_view_is_not_registered(router):
    with pytest.raises(Http404):
        router.route("test_view")
