import customtkinter as ctk


class DataDisplay(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        #config ul frameului
        self.configure(border_width=2, border_color='gray')
        self.label = ctk.CTkLabel(self, text='Afisare Date', font=("Franklin Gothic Book", 16))
        self.label.pack(pady=(10,20))

        #text box
        self.data_text = ctk.CTkTextbox(self, width=300, height=150)
        self.data_text.pack(pady=10)
        self.data_text.insert("0.0", "Datele...")