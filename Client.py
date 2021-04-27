import socket


class Client:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5555
    connected = False

    def __init__(self):
        self.client.settimeout(0.1)

    def is_connected(self):
        return self.connected

    def connect(self, ip_add):
        try:
            self.client.connect((ip_add, self.port))
            self.connected = True
        except socket.error:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error:
            pass

    def receive(self, msg_len):
        try:
            return self.client.recv(msg_len).decode()
        except socket.timeout:
            return ""
