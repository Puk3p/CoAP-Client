import customtkinter as ctk


class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Input", prompt="Introduceți textul:", callback=None):
        super().__init__(parent)
        self.callback = callback
        self.geometry("300x150")
        self.title(title)
        self.resizable(False, False)
        self.configure(bg="#2b2b2b")

        self.prompt_label = ctk.CTkLabel(self, text=prompt, font=("Franklin Gothic Book", 14), anchor="w")
        self.prompt_label.pack(pady=(20, 10), padx=20, fill="x")

        self.input_entry = ctk.CTkEntry(self, font=("Franklin Gothic Book", 12))
        self.input_entry.pack(pady=(0, 20), padx=20, fill="x")
        self.input_entry.focus()

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10, fill="x")

        self.ok_button = ctk.CTkButton(self.button_frame, text="OK", command=self.on_ok, fg_color="#00cc66")
        self.ok_button.pack(side="left", padx=(40, 10))

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.on_cancel, fg_color="#cc3333")
        self.cancel_button.pack(side="right", padx=(10, 40))

    def on_ok(self):
        if self.callback:
            self.callback(self.input_entry.get())
        self.destroy()

    def on_cancel(self):
        if self.callback:
            self.callback(None)
        self.destroy()
