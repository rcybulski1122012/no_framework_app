import selectors
import socket
from types import SimpleNamespace


class Server:
    def __init__(self, host, port, request_handler, *, encoding="utf-8"):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.sel = selectors.DefaultSelector()
        self.request_handler = request_handler

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(False)
        self.sel.register(self.s, selectors.EVENT_READ, data=None)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen()

    def __del__(self):
        self.s.close()

    def run(self):
        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.handle_new_client(key)
                else:
                    self.service_connection(key, mask)

    def handle_new_client(self, key):
        conn, addr = key.fileobj.accept()
        conn.setblocking(False)
        data = SimpleNamespace(addr=addr, request=b"", response=b"")
        self.sel.register(conn, selectors.EVENT_READ, data=data)

    def service_connection(self, key, mask):
        conn = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = conn.recv(4096)
            data.request += recv_data
            if self._is_request_fully_received(data.request) or not recv_data:
                data.response = self.request_handler(data.request)
                self.sel.modify(conn, selectors.EVENT_WRITE, data=data)

        if mask & selectors.EVENT_WRITE:
            if data.response:
                sent = conn.send(data.response)
                data.response = data.response[sent:]
            else:
                self.sel.unregister(conn)
                conn.close()

    def _is_request_fully_received(self, request):
        request = request.decode(self.encoding)
        request = request.replace("\r", "")
        if "\n\n" not in request:
            return False
        else:
            request_and_headers, body = request.split("\n\n")
            for line in request_and_headers.split("\n"):
                if "content-length" in line.lower():
                    content_length = int(line.split(":")[1].strip())
                    break
            else:
                return True

            content = request.split("\n\n", 1)[1]
            return len(content) == content_length
