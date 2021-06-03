from app.core.http import RequestHandler, Router, Server
from app.urls import urls

router = Router(urls)
handler = RequestHandler(router=router)
server = Server(host="127.0.0.1", port=8000, request_handler=handler)
server.run()
