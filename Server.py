import socket


class Server:
    server = socket.gethostbyname(socket.gethostname())
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connected_client = None

    def __init__(self):
        pass

    def get_ip(self):
        self.s.settimeout(0.001)
        return self.server

    def start_connection(self, ip_address):
        # bind the socket with the ip address (server) and port
        try:
            self.s.bind((ip_address, self.port))
        except socket.error:
            pass

        self.s.listen()

    def listen(self):
        try:
            self.connected_client, addr = self.s.accept()
            self.connected_client.settimeout(0.1)
        except socket.timeout:
            pass

    def is_connected(self):
        return self.connected_client is not None

    def send(self, data):
        try:
            self.connected_client.send(str.encode(data))
        except socket.timeout:
            pass

    def receive(self, msg_len):
        try:
            return self.connected_client.recv(msg_len).decode()
        except socket.timeout:
            return ""
