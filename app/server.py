import socket


class Server:
    def __init__(self, host, port, *, buff_size=1024, encoding="utf-8"):
        self.host = host
        self.port = port
        self.buff_size = buff_size
        self.encoding = encoding

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen()

    def __del__(self):
        self.s.close()

    def listen_for_client(self):
        conn, addr = self.s.accept()
        return conn, addr

    def receive_request(self, conn):
        request = b""
        while True:
            part = conn.recv(self.buff_size)
            request += part
            if len(part) < self.buff_size:
                break

        return request.decode(self.encoding)

    def send_response(self, conn, response):
        conn.sendall(response.encode(self.encoding))
