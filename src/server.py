import socket
import threading


class Server:
    def __init__(self, host, port, buff_size, *, encoding="utf-8"):
        self.host = host
        self.port = port
        self.buff_size = buff_size
        self.encoding = encoding

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen()

        with open("templates/index.html") as f:
            self.index = f.read()

    def __del__(self):
        self.s.close()

    def run(self):
        while True:
            conn, addr = self.s.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        with conn:
            request = self.receive_request(conn)
            response = self.handle_request(request)
            conn.sendall(b"HTTP/1.1 200 OK\n\n" + response)

    def receive_request(self, conn):
        request = b""
        while True:
            part = conn.recv(self.buff_size)
            request += part
            if len(part) < self.buff_size:
                break

        return request.decode(self.encoding)

    def handle_request(self, request):
        page = self.index.format(request)
        return page.encode(self.encoding)


if __name__ == '__main__':
    server = Server("127.0.0.1", 8000, 1024)
    server.run()
