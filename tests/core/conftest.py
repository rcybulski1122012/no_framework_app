import pytest

from app.core.request_handler import RequestHandler
from app.core.request_parser import HttpRequest
from app.core.response import HttpResponse
from app.core.router import Router


@pytest.fixture
def view(**kwargs):
    return lambda request: HttpResponse("HTTP/1.1", 200, "OK", {}, "Test view")


@pytest.fixture
def router():
    return Router({})


@pytest.fixture
def GET_request_obj():
    return HttpRequest(
        b"GET /hello.htm?first=1&second=2 HTTP/1.1\n"
        b"Host: www.host.com\n"
        b"Accept-Language: en-us\n"
    )


@pytest.fixture
def handler(router, view):
    router.routes = {"/test": view}
    return RequestHandler(router)
