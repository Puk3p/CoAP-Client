import os
from itertools import cycle
from tkinter import Menu, simpledialog, messagebox, filedialog
import chardet
import customtkinter as ctk

from PIL import Image
import tkinter as tk
from customtkinter import CTkImage

from GUI.components.DinoAnimation import DinoAnimation
from GUI.styles.CustomDialog import CustomDialog
from coap_client.client import CoAPClient


class FileExplorer(ctk.CTkFrame):
    def __init__(self, parent, host, port):
        super().__init__(parent)
        self.client = CoAPClient(host=host, port=port)
        self.current_path = "/"  # root
        self.configure(border_width=2, border_color="gray")

        self.animation_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.animation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.text_label = ctk.CTkLabel(
            self.animation_frame,
            text="Eu sunt Niki! Asistenul tău virtual! \nTestează butonul de Upload sau Create!",
            font=("Franklin Gothic Book", 18),
            text_color="white",
            anchor="center",
        )
        self.text_label.pack()

        self.canvas = tk.Canvas(self.animation_frame, width=200, height=200, bg="#333333", highlightthickness=0)
        self.canvas.pack()

        assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.assets/cat"))

        self.dino_animation = DinoAnimation(self.canvas, assets_path, x=60, y=60, scale=3, fps=10)
        self.dino_animation.start_animation()

        self.message_type_var = ctk.StringVar(value="CON")
        self.message_type_label = ctk.CTkLabel(self, text="Message Type:", font=("Franklin Gothic Book", 14))
        self.message_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.con_radio = ctk.CTkRadioButton(self, text="Confirmable (CON)",
                                            variable=self.message_type_var, value="CON")
        self.con_radio.grid(row=1, column=1, padx=(10, 5), pady=10)

        self.non_radio = ctk.CTkRadioButton(self, text="Non-confirmable (NON)",
                                            variable=self.message_type_var, value="NON")
        self.non_radio.grid(row=1, column=2, padx=(5, 10), pady=10)

        self.control_bar = ctk.CTkFrame(self)
        self.control_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

        self.create_button = self.create_animated_button(self.control_bar, "Create", self.create_file)
        self.create_button.pack(side="left", padx=(10, 5))

        self.upload_button = self.create_animated_button(self.control_bar, "Upload", self.upload_file)
        self.upload_button.pack(side="left", padx=(5, 5))

        self.back_button = self.create_animated_button(self.control_bar, "Go Back", self.go_back)
        self.back_button.pack(side="right", padx=(5, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=700, height=450)
        self.scroll_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)

        self.icons = {
            "json": CTkImage(light_image=Image.open(".assets/json.png"), size=(32, 32)),
            "db": CTkImage(light_image=Image.open(".assets/db.png"), size=(32, 32)),
            "jar": CTkImage(light_image=Image.open(".assets/jar.png"), size=(32, 32)),
            "sh": CTkImage(light_image=Image.open(".assets/sh.png"), size=(32, 32)),
            "yml": CTkImage(light_image=Image.open(".assets/yml.png"), size=(32, 32)),
            "txt": CTkImage(light_image=Image.open(".assets/txt.png"), size=(32, 32)),
            "default": CTkImage(light_image=Image.open(".assets/file_icon.png"), size=(32, 32)),
            "folder": CTkImage(light_image=Image.open(".assets/folder.png"), size=(32, 32)),
            "zip": CTkImage(light_image=Image.open(".assets/zip.png"), size=(32, 32)),
        }

        self.border_colors = cycle(["#1e90ff", "#32cd32", "#ff4500", "#ff1493", "#ffd700"])
        self.frames = []

        # Actualizare
        self.update_files()

    def get_message_type(self):
        return 0 if self.message_type_var.get() == "CON" else 1

    def create_animated_button(self, parent, text, command):
        button = ctk.CTkButton(parent, text=text, font=("Franklin Gothic Book", 14), command=command, width=100)

        def on_enter(event):
            button.configure(fg_color="#f1ff00")  # Culoare de hover
            self.pulse_animation(button)

        def on_leave(event):
            button.configure(fg_color="#ff7fe4")  # Revenire la culoarea de bază
            button.after_cancel(getattr(button, "pulse_job", None))  # Oprește pulsarea

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def pulse_animation(self, button):
        current_color = button.cget("fg_color")
        if current_color == "#00cc99":
            button.configure(fg_color="#00ffcc")  # Mai deschis
        else:
            button.configure(fg_color="#00cc99")  # Mai închis

        button.pulse_job = button.after(500, lambda: self.pulse_animation(button))

    def create_file(self):
        file_name = simpledialog.askstring("Create File", "Introduceți numele fișierului:")
        if file_name:
            self.send_put_request(file_name, "")

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    raw_data = file.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected["encoding"] or "latin1"
                    content = raw_data.decode(encoding)  
                    file_name = os.path.basename(file_path)
                    self.send_put_request(file_name, content)
            except UnicodeDecodeError as e:
                messagebox.showerror("Eroare", f"Eroare la decodarea fișierului: {e}")
            except Exception as e:
                messagebox.showerror("Eroare", f"A apărut o eroare: {e}")

    def get_icon(self, file_name):
        if "." in file_name:
            extension = file_name.split(".")[-1].lower()
            return self.icons.get(extension, self.icons["default"])
        return self.icons["folder"]

    def send_put_request(self, file_name, content):
        message_type = self.get_message_type()  # CON sau NON
        response = self.client.send_request(
            message_type=message_type,
            code=3,  # PUT
            message_id=12348,
            token=b"",
            options=[(11, f"{self.current_path}/{file_name}".encode())],
            payload=content.encode()
        )

        if response and response.code in (65, 68):  # 2.01 Created sau 2.04 Changed
            self.display_animation(response.payload.decode(), "success")
            self.update_files()
        else:
            error_msg = response.payload.decode() if response else "No response from server."
            self.display_animation(f"Eroare PUT: {error_msg}", "error")

    def update_files(self):
        try:
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            message_type = self.get_message_type()

            response = self.client.send_request(
                message_type=message_type,
                code=1,  # GET
                message_id=12345,  # ID unic pentru cerere
                token=b"",  # Fără token
                options=[(11, self.current_path.encode())],
                payload=b""
            )

            if message_type == 1:  # NON
                if not response:
                    self.display_animation("Mesaj Non-confirmable trimis. Nu se așteaptă răspuns.", "error")
                    return

            if not response.payload.strip():
                raise ValueError("Folderul este gol sau răspunsul este invalid!")

            self.display_files(response.payload.decode())
        except Exception as e:
            self.display_error(f"Eroare: {e}")

    def display_files(self, response):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        files = response.split("\n")
        visible_files = [file for file in files if not file.startswith(".")]

        self.frames = []
        row, col = 0, 0
        for file in visible_files:
            frame = ctk.CTkFrame(
                self.scroll_frame,
                border_width=2,
                border_color="gray"
            )
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.frames.append(frame)

            icon = self.get_icon(file)

            label_icon = ctk.CTkLabel(frame, image=icon, text="")
            label_icon.pack(pady=(5, 0))

            label_name = ctk.CTkLabel(frame, text=file, font=("Franklin Gothic Book", 12))
            label_name.pack(pady=(5, 5))

            frame.bind("<Button-3>", lambda event, f=file: self.show_context_menu(event, f))

            if "." not in file:  # Este un folder
                open_button = ctk.CTkButton(
                    frame, text="Open", font=("Franklin Gothic Book", 10),
                    command=lambda f=file: self.change_directory(f)
                )
                open_button.pack()

            col += 1
            if col > 3:
                col = 0
                row += 1

        self.animate_borders()

    def show_context_menu(self, event, file_name):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Delete", command=lambda: self.delete_file(file_name))
        menu.add_command(label="Rename", command=lambda: self.rename_file(file_name))
        menu.post(event.x_root, event.y_root)

    def delete_file(self, file_name):
        message_type = self.get_message_type()
        response = self.client.send_request(
            message_type=message_type,
            code=4,
            message_id=12346,
            token=b"",
            options=[(11, f"{self.current_path}/{file_name}".encode())],
            payload=b""
        )

        if response and response.code == 66:
            self.display_animation(f"Fișierul '{file_name}' a fost șters!", "success")
            self.update_files()
        else:
            error_msg = response.payload.decode() if response and response.payload else "No response from server."
            self.display_animation(f"Ștergerea a eșuat: {error_msg}", "error")

    def display_animation(self, message, animation_type):
        frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10,
                             fg_color="green" if animation_type == "success" else "red")
        frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=message, font=("Franklin Gothic Book", 14), text_color="white")
        label.grid(row=0, column=0, padx=10, pady=10)

        def remove_animation():
            if frame.winfo_exists():
                frame.destroy()

        frame.after(2000, remove_animation)

    def rename_file(self, file_name):
        def on_submit(new_name):
            if new_name:
                payload = f"{file_name}::{new_name}".encode()
                message_type = self.get_message_type()
                response = self.client.send_request(
                    message_type=message_type,
                    code=2,  # POST
                    message_id=12347,
                    token=b"",
                    options=[(11, self.current_path.encode())],
                    payload=payload
                )
                if response and response.code == 68:
                    self.display_animation("Fișier redenumit cu succes!", "success")
                    self.update_files()
                else:
                    error_msg = response.payload.decode() if response else "No response from server."
                    self.display_animation(f"Eroare la redenumire: {error_msg}", "error")
            else:
                self.display_animation("Redenumirea a fost anulată.", "error")

        CustomDialog(self, title="Redenumire fișier", prompt=f"Introduceți noul nume pentru '{file_name}':",
                     callback=on_submit)

    def animate_borders(self):
        next_color = next(self.border_colors)
        valid_frames = []
        for frame in self.frames:
            if frame.winfo_exists():
                frame.configure(border_color=next_color)
                valid_frames.append(frame)
        self.frames = valid_frames
        self.after(1500, self.animate_borders)

    def display_error(self, message):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        error_label = ctk.CTkLabel(self.scroll_frame, text=message, font=("Franklin Gothic Book", 14), fg_color="red")
        error_label.pack()

    def change_directory(self, folder_name):
        self.current_path = f"{self.current_path}/{folder_name}".replace("//", "/")
        self.update_files()

    def go_back(self):
        if self.current_path != "/":
            self.current_path = "/".join(self.current_path.split("/")[:-1])
            self.update_files()
