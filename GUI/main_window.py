from itertools import cycle
import customtkinter as ctk

from GUI.components.file_display import FileExplorer


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("MainWindow inițializată!")

        self.title("CoAP Client")
        self.geometry("1300x800")
        self.resizable(False, False)
        self.setup_ui()

        self.border_colors = cycle(["#1e90ff", "#32cd32", "#ff4500", "#ff1493", "#ffd700"])
        self.animate_borders()

    def setup_ui(self):
        header = ctk.CTkLabel(self, text="CoAP Client", font=("Franklin Gothic Book", 24))
        header.pack(pady=10)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.file_explorer_frame = FileExplorer(main_frame, host="136.243.153.183", port=8080)
        self.file_explorer_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.log_frame = ctk.CTkFrame(main_frame, width=300)
        self.log_frame.pack(side="right", fill="y", padx=10)

        log_label = ctk.CTkLabel(self.log_frame, text="Log activitate", font=("Franklin Gothic Book", 16))
        log_label.pack(pady=10)

        self.log_text = ctk.CTkTextbox(self.log_frame, width=300, height=500)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_text.insert("0.0", "Conectat la server.\n")

        # Bara de stare
        self.status_bar = ctk.CTkLabel(self, text="Stare: Conectat", font=("Franklin Gothic Book", 12), anchor="w")
        self.status_bar.pack(fill="x", pady=(5, 0))

    #animatii terminat
    def animate_borders(self):
        next_color = next(self.border_colors)

        self.file_explorer_frame.configure(border_color=next_color)
        self.log_frame.configure(border_color=next_color)

        self.after(500, self.animate_borders)

    #nu i gata e beta
    def update_log(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    #dracu sa ma ia, inca nu i gt
    def update_status(self, status):
        self.status_bar.configure(text=f"Stare: {status}")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
