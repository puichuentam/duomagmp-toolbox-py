import socket
from datetime import datetime

class NetSender:
    def __init__(self, host="255.255.255.255", port=5005, use_tcp=False):
        self.host = host
        self.port = port
        self.use_tcp = use_tcp
        if use_tcp:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, coil_label):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        msg = f"{ts} | PULSE | Coil={coil_label}"
        data = msg.encode("utf-8")
        if self.use_tcp:
            self.sock.sendall(data)
        else:
            self.sock.sendto(data, (self.host, self.port))

    def close(self):
        self.sock.close()
