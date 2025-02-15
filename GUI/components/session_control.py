import customtkinter as ctk


class SessionControl(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(border_width=2, border_color="gray")
        self.label = ctk.CTkLabel(self, text="Session Control", font=("Franklin Gothic Book", 16))
        self.label.pack(pady=(10, 20))

        self.create_button = ctk.CTkButton(self, text="Session Create", command=self.create_session)
        self.create_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Session Delete", command=self.delete_session)
        self.delete_button.pack(pady=10)

    def create_session(self):
        print("Session created")

    def delete_session(self):
        print("Session deleted")

    def pack(self):
        pass