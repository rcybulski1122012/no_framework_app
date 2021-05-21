import pytest
from app.http_handling import HttpRequest


GET_request = ("GET /hello.htm HTTP/1.1\n"
               "Host: www.host.com\n"
               "Accept-Language: en-us\n")

POST_request = ("POST /cgi-bin/process.cgi HTTP/1.1\n"
                "Host: www.host.com\n"
                "Content-Type: application/x-www-form-urlencoded\n"
                "Content-Length: length\n"
                "Accept-Language: en-us\n\n"
                "licenseID=string&content=string&/paramsXML=string")


GET_request_test_data = [
    ("method", "GET"),
    ("path", "/hello.htm"),
    ("version", "HTTP/1.1"),
    ("headers", {"Host": "www.host.com", "Accept-Language": "en-us"}),
    ("body", ""),
]

POST_request_test_data = [
    ("method", "POST"),
    ("path", "/cgi-bin/process.cgi"),
    ("version", "HTTP/1.1"),
    ("headers", {
        "Host": "www.host.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "length",
        "Accept-Language": "en-us",
    }),
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
