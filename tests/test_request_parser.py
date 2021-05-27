import pytest

from app.core.errors import Http400
from app.core.request_parser import HttpRequest

GET_request = (
    b"GET /hello.htm?first=1&second=2 HTTP/1.1\n" b"Host: www.host.com\n" b"Accept-Language: en-us\n"
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
    ("headers", {"host": "www.host.com", "accept-language": "en-us"}),
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


@pytest.mark.parametrize("element,expected", GET_request_test_data)
def test_HttpRequest_GET_request(element, expected):
    request = HttpRequest(GET_request)
    assert getattr(request, element) == expected


@pytest.mark.parametrize("element,expected", POST_request_test_data)
def test_HttpRequest_POST_request(element, expected):
    request = HttpRequest(POST_request)
    assert getattr(request, element) == expected


def test_HttpRequest_raises_exception_when_bad_request():
    request = b"BAD REQUEST"
    with pytest.raises(Http400):
        HttpRequest(request)
