from app.request_handler import RequestHandler
from app.request_parser import HttpRequest
from app.router import Router
from app.server import Server

router = Router()
handler = RequestHandler(router=router)


@router.register_view("/")
def index(request):
    return f"Index\nHost: {request.headers['Host']}"


@router.register_view("/hello")
def hello(request):
    return "Hello"


server = Server(host="127.0.0.1", port=8000, request_handler=handler)
server.run()
