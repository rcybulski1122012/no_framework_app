import pytest

from app.core.http.errors import InvalidRequestFormat
from app.core.http.request import HttpRequest
from app.core.http.sessions import Session

GET_request = (
    b"GET /hello.htm?first=1&second=2 HTTP/1.1\n"
    b"Host: www.host.com\n"
    b"Cookie: first=1; second=2; third=3\n"
    b"Accept-Language: en-us\n"
)

POST_request = (
    b"POST /cgi-bin/process.cgi HTTP/1.1\n"
    b"Host: www.host.com\n"
    b"Content-Type: application/x-www-form-urlencoded\n"
    b"Content-Length: length\n"
    b"Accept-Language: en-us\n\n"
    b"licenseID=string&content=string&/paramsXML=string\n"
)


GET_request_test_data = [
    ("method", "GET"),
    ("path", "/hello.htm"),
    ("params", {"first": "1", "second": "2"}),
    ("version", "HTTP/1.1"),
    (
        "headers",
        {
            "host": "www.host.com",
            "accept-language": "en-us",
            "cookie": "first=1; second=2; third=3",
        },
    ),
    ("cookies", {"first": "1", "second": "2", "third": "3"}),
    ("body", ""),
]

POST_request_test_data = [
    ("method", "POST"),
    ("path", "/cgi-bin/process.cgi"),
    ("params", {}),
    ("version", "HTTP/1.1"),
    (
        "headers",
        {
            "host": "www.host.com",
            "content-type": "application/x-www-form-urlencoded",
            "content-length": "length",
            "accept-language": "en-us",
        },
    ),
    ("body", "licenseID=string&content=string&/paramsXML=string"),
]


def test_request_without_body_and_headers():
    request = HttpRequest(b"GET / HTTP/1.1\n")
    assert (request.method, request.path, request.version) == ("GET", "/", "HTTP/1.1")


@pytest.mark.parametrize("element,expected", GET_request_test_data)
def test_request_without_body(element, expected):
    request = HttpRequest(GET_request)
    assert getattr(request, element) == expected


@pytest.mark.parametrize("element,expected", POST_request_test_data)
def test_request_with_body(element, expected):
    request = HttpRequest(POST_request)
    assert getattr(request, element) == expected


def test_raises_exception_when_bad_request():
    request = b"BAD REQUEST"
    with pytest.raises(InvalidRequestFormat):
        HttpRequest(request)
