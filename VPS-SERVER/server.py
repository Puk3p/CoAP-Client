import os
import socket
from packet import CoAPPacket 

ALLOWED_IPS = ["81.180.218.61", "81.180.218.60"]  # IP conexiuni


def handle_request(data, addr, server):
    current_path = os.getcwd()
    print(f"[Server] Pachet primit de la {addr}")

    try:
        packet = CoAPPacket.parse(data)
        print(f"[Server] Header: Version={packet.version}, Type={packet.message_type}, Code={packet.code}")
        print(f"[Server] Token: {packet.token}, Options: {packet.options}, Payload: {packet.payload.decode() if packet.payload else '<empty>'}")

        send_ack = packet.message_type == 0  #trimitem pt CON
        #(GET, POST, PUT, DELETE)
        if packet.code == 1:  # GET (Listare directoare)
            folder_path = "/"
            for option_delta, option_value in packet.options:
                if option_delta == 11:  # Uri-Path
                    folder_path = option_value.decode()

            full_path = os.path.join(current_path, folder_path.strip("/"))
            if os.path.isdir(full_path):
                files = [f for f in os.listdir(full_path) if not f.startswith(".")]
                response_payload = "\n".join(files).encode()
                response_code = 69  # 2.05 Content
            else:
                response_payload = "Directory not found".encode()
                response_code = 132  # 4.04 Not Found

        elif packet.code == 2:  # POST (Redenumire)
            try:
                old_name, new_name = packet.payload.decode().split("::")
                folder_path = "/"
                for option_delta, option_value in packet.options:
                    if option_delta == 11:  # Uri-Path
                        folder_path = option_value.decode().strip("/")

                old_path = os.path.join(current_path, folder_path, old_name.strip())
                new_path = os.path.join(current_path, folder_path, new_name.strip())

                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    response_payload = f"Resource renamed from '{old_name}' to '{new_name}'".encode()
                    response_code = 68  # 2.04 Changed
                else:
                    response_payload = f"Resource '{old_name}' not found.".encode()
                    response_code = 132  # 4.04 Not Found
            except Exception as e:
                response_payload = f"Error renaming resource: {e}".encode()
                response_code = 128  # 4.00 Bad Request

        elif packet.code == 3:  # PUT 
            file_name = ""
            for option_delta, option_value in packet.options:
                if option_delta == 11:  # Uri-Path
                    file_name = option_value.decode()

            file_path = os.path.join(current_path, file_name.strip("/"))
            try:
                with open(file_path, "w") as f:
                    f.write(packet.payload.decode())
                response_payload = f"File '{file_name}' created or updated successfully.".encode()
                response_code = 68  # 2.04 Changed
            except Exception as e:
                response_payload = f"Error processing PUT request: {e}".encode()
                response_code = 128  # 4.00 Bad Request

        elif packet.code == 4:  # DELETE 
            file_name = ""
            for option_delta, option_value in packet.options:
                if option_delta == 11:  # Uri-Path
                    file_name = option_value.decode()

            file_path = os.path.normpath(os.path.join(current_path, file_name.strip("/")))
            if os.path.exists(file_path):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                    response_payload = "Resource deleted".encode()
                    response_code = 66  # 2.02 Deleted
                except Exception as e:
                    response_payload = f"Error deleting resource: {e}".encode()
                    response_code = 128  # 4.00 Bad Request
            else:
                response_payload = "Resource not found".encode()
                response_code = 132  # 4.04 Not Found

        else:
            response_payload = "Invalid request".encode()
            response_code = 128  # 4.00 Bad Request

        if send_ack:
            response_packet = CoAPPacket(
                version=1,
                message_type=2,  # Ack
                tkl=len(packet.token),
                code=response_code,
                message_id=packet.message_id,
                token=packet.token,
                payload=response_payload
            )
            server.sendto(response_packet.build(), addr)
            print(f"[Server] Raspuns trimis către {addr}: {response_payload.decode()}")
        else:
            print("[Server] Non-confirmable mesaj procesat fără răspuns.")

    except Exception as e:
        print(f"[Server] Eroare la procesarea pachetului: {e}")
        if packet.message_type == 0:  # Trimitem răspuns de eroare doar pentru CON
            response_payload = f"Malformed packet: {e}".encode()
            response_packet = CoAPPacket(
                version=1,
                message_type=2,  # Acknowledgement
                tkl=0,
                code=128,  # 4.00 Bad Request
                message_id=0,  # ID arbitrar
                payload=response_payload
            )
            server.sendto(response_packet.build(), addr)
            print(f"[Server] Răspuns de eroare trimis către {addr}: {response_payload.decode()}")


def start_server(host="0.0.0.0", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print(f"Server listening on {host}:{port}")

    while True:
        data, addr = server.recvfrom(4096)
        client_ip = addr[0]

        if client_ip in ALLOWED_IPS:
            print(f"[Server] Conexiune permisă de la {client_ip}")
            handle_request(data, addr, server)
        else:
            print(f"[Server] Conexiune refuzată pentru {client_ip}")


if __name__ == "__main__":
    start_server()
