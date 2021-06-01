def get_request(path):
    return f"GET {path} HTTP/1.1\n".encode("utf-8")


def test_proper_request(handler):
    expected = b"HTTP/1.1 200 OK\n\nTest view\n"
    request = get_request("/test")
    assert handler(request) == expected


def test_returns_400_when_bad_request(handler):
    expected = b"HTTP/1.1 400 Bad Request\n"
    assert handler(b"BAD REQUEST") == expected


def test_returns_404_when_invalid_path(handler):
    expected = b"HTTP/1.1 404 Not Found\n"
    request = get_request("/invalid/path")
    assert handler(request) == expected


def test_returns_500_when_unexpected_error(handler, monkeypatch):
    def stub(self, request):
        assert False

    expected = b"HTTP/1.1 500 Internal Server Error\n"
    request = get_request("/test")
    monkeypatch.setattr(handler, "_handle_request", stub)

    assert handler(request) == expected
