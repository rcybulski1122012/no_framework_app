from app.core.http.decorators import POST_required


def test_POST_required_does_nothing_when_request_POST(view, POST_request_obj):
    expected = view(None)
    view = POST_required(view)
    result = view(POST_request_obj)

    assert result.get_response() == expected.get_response()


def test_POST_required_returns_405_when_different_method(view, GET_request_obj):
    view = POST_required(view)
    expected = b"HTTP/1.1 405 Method Not Allowed\n"
    result = view(GET_request_obj)

    assert result.get_response() == expected
