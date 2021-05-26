import pytest

from app.core.request_handler import RequestHandler


@pytest.fixture
def handler(router, view):
    router.register_view("/test")(view)
    return RequestHandler(router)


def get_request(path):
    return f"GET {path} HTTP/1.1\n".encode("utf-8")


def test_handle_request(handler):
    expected = b"HTTP/1.1 200 OK\n\nTest view"
    request = get_request("/test")
    assert handler(request) == expected


def test_returns_400_when_bad_request(handler):
    expected = b"HTTP/1.1 400 BAD REQUEST\n"
    assert handler(b"BAD REQUEST") == expected


def test_returns_404_when_invalid_path(handler):
    expected = b"HTTP/1.1 404 NOT FOUND\n"
    request = get_request("/invalid/path")
    assert handler(request) == expected
