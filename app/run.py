from core.request_handler import RequestHandler
from core.router import Router
from core.server import Server
from core.templates import render_template

router = Router()
handler = RequestHandler(router=router)


@router.register_view("/", "text/html")
def index(request):
    return render_template("index.html", title="Hello world!")


@router.register_view("/hello", "text/html")
def hello(request):
    return "Hello"


server = Server(host="127.0.0.1", port=8000, request_handler=handler)
server.run()
