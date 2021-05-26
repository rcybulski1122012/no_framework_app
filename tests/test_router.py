import pytest

from app.core.errors import Http404


def test_register_view(router, view):
    router.register_view("/test")(view)
    assert router.views["/test"] == view


def test_route(router, view):
    router.register_view("/test")(view)
    assert view == router.route("/test")


def test_route_raises_exception_when_view_is_not_registered(router):
    with pytest.raises(Http404):
        router.route("test_view")
