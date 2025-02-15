import customtkinter as ctk

class RequestForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(border_width=2, border_color='gray')
        self.label = ctk.CTkLabel(self, text="Request Form", font=("Franklin Gothic Book", 16))
        self.label.pack(pady=(10, 20))

        self.uri_entry = ctk.CTkEntry(self, placeholder_text="URL")  #
        self.uri_entry.pack(pady=10)

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_request)
        self.send_button.pack(pady=10)

    def send_request(self):
        uri = self.uri_entry.get()
        print(f"Requesting {uri}")
