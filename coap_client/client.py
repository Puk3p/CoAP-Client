import os
import socket
from coap_client.packet import CoAPPacket as Packet

class CoAPClient:
    def __init__(self, host=None, port=None, timeout=5):
        self.host = host or os.getenv("COAP_SERVER_HOST", "127.0.0.1")
        self.port = int(port or os.getenv("COAP_SERVER_PORT", "8080"))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        print(f"[Client] Conectat la {self.host} : {self.port}")

    def send_request(self, message_type, code, message_id, token=None, options=None, payload=None):
        # Crearea
        packet = Packet(
            version=1,
            message_type=message_type,
            tkl=len(token) if token else 0,
            code=code,
            message_id=message_id,
            token=token,
            options=options,
            payload=payload
        )

        # Construim
        built_packet = packet.build()
        print(f"[Client] Pachet construit: {built_packet}")

        # Trimitem
        self.socket.sendto(built_packet, (self.host, self.port))
        print(f"[Client] Pachet trimis către {self.host}:{self.port}")

        # IES daca e NON
        if message_type == 1:  # NON
            print("[Client] Mesaj Non-confirmable trimis. Nu se așteaptă răspuns.")
            return None

        # Astept
        response, sender_address = self.socket.recvfrom(4096)
        print(f"[Client] Răspuns brut primit: {response}")

        # Decodific
        parsed_response = Packet.parse(response)
        print(f"[Client] Răspuns decodificat: {parsed_response}")

        return parsed_response

    def close(self):
        self.socket.close()
        print("[Client] Socket închis!")
