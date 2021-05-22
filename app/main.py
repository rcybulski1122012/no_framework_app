import threading

from server import Server
from http_handling import HttpRequest, InvalidHttpRequest


server = Server(host="127.0.0.1", port=8000)


def handle_client(conn, addr):
    with conn:
        request_string = server.receive_request(conn)
        try:
            request = HttpRequest(request_string)
        except InvalidHttpRequest:
            response = f"HTTP/1.1 400 Bad Request"
        else:
            response = f"HTTP/1.1 200 OK\n\n{request.request_string}"
        server.send_response(conn, response)


while True:
    connection, address = server.listen_for_client()
    threading.Thread(target=handle_client, args=(connection, address)).start()
