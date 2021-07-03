# def test_POST_required_does_nothing_when_request_POST(view, POST_request_obj):
#     expected = view(None)
#     view = POST_required(view)
#     result = view(POST_request_obj)
#
#     assert result.get_response() == expected.get_response()
#
#
# def test_POST_required_returns_405_when_different_method(view, GET_request_obj):
#     view = POST_required(view)
#     expected = b"HTTP/1.1 405 Method Not Allowed\n"
#     result = view(GET_request_obj)
#
#     assert result.get_response() == expected
import pytest

from app.core.errors import Http405
from app.core.http.decorators import http_method_required


def test_http_method_required_does_nothing_when_given_method(view, POST_request_obj):
    expected = view(None)
    view = http_method_required("POST")(view)
    result = view(POST_request_obj)

    assert result.get_response() == expected.get_response()


def test_http_method_required_raises_405_when_different_method(view, GET_request_obj):
    view = http_method_required("POST")(view)

    with pytest.raises(Http405):
        view(GET_request_obj)


def test_http_method_required_is_insensitive_for_letter_size(view, GET_request_obj):
    view = http_method_required("PoSt")(view)

    with pytest.raises(Http405):
        view(GET_request_obj)
