import os
from PIL import Image, ImageTk
from GUI.main_window import MainWindow
from coap_client.client import CoAPClient
from gateway.gateway import GateWay
import unittest
import customtkinter as ctk

def run_gui_tests():
    from tests.test_gui import TestGUIComponents
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGUIComponents))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)

def run_gui_application():
    print("Pornește GUI-ul...")
    app = MainWindow()
    app.mainloop()

def send_packet_to_server():
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", "8080"))
    
    client = CoAPClient(host=host, port=port)
    
    message_id = int(os.getenv("MESSAGE_ID", "12345"))
    token = os.getenv("TOKEN", "abcd").encode()
    options = [(11, os.getenv("URI_PATH", "uri-path").encode()), (12, os.getenv("OPTION_TEST", "test-option").encode())]
    payload = os.getenv("PAYLOAD", "Content to be sent as payload").encode()
    
    response = client.send_request(
        message_type=0,  # Confirmable
        code=2,  # POST
        message_id=message_id,
        token=token,
        options=options,
        payload=payload,
    )
    print(f"[Client] Răspuns primit: {response}")

def send_packet_to_local():
    host = "127.0.0.1"
    port = int(os.getenv("LOCAL_PORT", "6006"))
    
    client = CoAPClient(host=host, port=port)
    
    message_id = int(os.getenv("LOCAL_MESSAGE_ID", "67890"))
    token = os.getenv("LOCAL_TOKEN", "xyz").encode()
    options = [(11, os.getenv("LOCAL_URI_PATH", "local-path").encode()), (13, os.getenv("LOCAL_OPTION", "local-option").encode())]
    payload = os.getenv("LOCAL_PAYLOAD", "Local payload content").encode()
    
    response = client.send_request(
        message_type=0,  # Confirmable
        code=2,  # POST
        message_id=message_id,
        token=token,
        options=options,
        payload=payload,
    )
    print(f"[Client] Răspuns primit: {response}")

def start_gateway():
    host = os.getenv("GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("GATEWAY_PORT", "8080"))
    
    gateway = GateWay(host=host, port=port)
    gateway.listen()

def display_image():
    root = ctk.CTk()
    root.title("Afișare imagine")
    root.geometry("600x400")
    
    image_path = input("Introduceți calea imaginii: ").strip()
    try:
        img = Image.open(image_path)
        img_resized = img.resize((400, 300))
        img_tk = ImageTk.PhotoImage(img_resized)
        
        label = ctk.CTkLabel(root, image=img_tk, text="")
        label.image = img_tk
        label.pack(pady=20)
        
        root.mainloop()
    except FileNotFoundError:
        print("Imaginea nu a fost găsită. Verificați calea și încercați din nou.")

if __name__ == "__main__":
    print("Opțiuni disponibile:")
    print("1. Lansează aplicația GUI")
    print("2. Rulează testele GUI")
    print("3. Trimite pachet către server (dedicat)")
    print("4. Pornește Gateway-ul (forward către serverul dedicat)")
    print("5. Trimite pachet către calculatorul personal")
    print("6. Afișează o imagine folosind PIL")
    
    choice = input("Alege opțiunea (1/2/3/4/5/6): ").strip()
    
    if choice == "1":
        run_gui_application()
    elif choice == "2":
        run_gui_tests()
    elif choice == "3":
        send_packet_to_server()
    elif choice == "4":
        start_gateway()
    elif choice == "5":
        send_packet_to_local()
    elif choice == "6":
        display_image()
    else:
        print("Opțiune invalidă! Te rog alege 1, 2, 3, 4, 5 sau 6.")
