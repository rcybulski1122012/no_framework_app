from core.request_handler import RequestHandler
from core.router import Router
from core.server import Server

from app.urls import urls

router = Router(urls)
handler = RequestHandler(router=router)
server = Server(host="127.0.0.1", port=8000, request_handler=handler)
server.run()
