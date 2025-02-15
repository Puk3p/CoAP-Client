import socket
from config import SERVER_CONFIG


class GateWay:
    def __init__(self, host="0.0.0.0", port=SERVER_CONFIG["port"]):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"[Gateway] Pornit pe {host}:{port}")

    def listen(self):
        print("[Gateway] Ascultă cereri...")
        while True:
            data, sender_address = self.socket.recvfrom(1024)
            print(f"[Gateway] Primit de la {sender_address}: {data.decode()}")

            server_host = SERVER_CONFIG["host"]
            server_port = SERVER_CONFIG["port"]
            self.socket.sendto(data, (server_host, server_port))
            print(f"[Gateway] Forward către {server_host}:{server_port}")