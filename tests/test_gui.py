import unittest
import customtkinter as ctk

# Importam componentele de la interfata grafica
from GUI.components import SessionControl, DataDisplay, RequestForm


class TestGUIComponents(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.root.geometry('800x600')

    def tearDown(self):
        self.root.destroy()

    def test_session_control_creation(self):
        session_control = SessionControl(self.root)
        session_control.pack()
        self.assertIsNotNone(session_control, "Componenta SessionControl nu a reusit sa se initializeze.")
        print("Componenta SessionControl a fost initializata cu succes.")

    def test_data_display_creation(self):
        data_display = DataDisplay(self.root)
        data_display.pack()
        self.assertIsNotNone(data_display, "Componenta DataDisplay nu a reusit sa se initializeze.")
        print("Componenta DataDisplay a fost initializata cu succes.")

    def test_request_form_creation(self):
        request_form = RequestForm(self.root)
        request_form.pack()
        self.assertIsNotNone(request_form, "Componenta RequestForm nu a reusit sa se initializeze.")
        print("Componenta RequestForm a fost initializata cu succes.")

    def test_session_control_buttons(self):
        session_control = SessionControl(self.root)
        session_control.pack()
        session_control.create_button.invoke()
        session_control.delete_button.invoke()
        print("Butoanele din componenta SessionControl functioneaza corect.")

if __name__ == "__main__":
    unittest.main()
