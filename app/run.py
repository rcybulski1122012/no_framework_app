from app.core.http.request_handler import RequestHandler
from app.core.http.router import Router
from app.core.http.server import Server
from app.urls import urls


router = Router(urls)
handler = RequestHandler(router=router)
server = Server(host="127.0.0.1", port=8000, request_handler=handler)
server.run()
