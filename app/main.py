from server import Server
from http_handling import HttpRequest, InvalidHttpRequest


def fake_handler(request):
    return b"HTTP/1.1 200 OK\n\nHello world\n"


server = Server(host="127.0.0.1", port=8000, request_handler=fake_handler)
server.run()
