import tkinter as tk
from tkinter import messagebox
from servicemanager import ServiceManagerApp
from app_rebuilder import rebuild_app
from report_generator import generate_reports
import subprocess
import os
from config import business_name
class MainApp:
    def __init__(self, root):
        self.root = root

        root.title(f"Automated {business_name} Report Service")

        # Increase the window size
        root.geometry("1000x700")  # Adjust the dimensions as needed

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Create a submenu for service management
        self.service_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Service", menu=self.service_menu)
        self.service_menu.add_command(label="Manage Service", command=self.open_service_manager)

        # Create a submenu for configuration editing
        self.config_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Config", menu=self.config_menu)
        self.config_menu.add_command(label="Edit Config", command=self.open_config_editor)

        # Create a submenu for sending email
        self.email_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Email", menu=self.email_menu)
        self.email_menu.add_command(label="Send Email Now", command=self.send_email_now)

        # Get the current working directory
        current_directory = os.getcwd()

        # Get a list of all .py files in the code base directory
        code_files = [f for f in os.listdir(current_directory) if f.endswith(".py")]

        # Create a submenu for the code base
        self.code_base_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Code Base", menu=self.code_base_menu)

        # Create a submenu for rebuilding the app
        self.rebuild_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Rebuild", menu=self.rebuild_menu)
        self.rebuild_menu.add_command(label="Rebuild App", command=self.call_rebuild_app)

        # Add subitems for each code file
        for code_file in code_files:
            self.code_base_menu.add_command(label=code_file, command=lambda file=code_file: self.open_code_file(current_directory, file))

        # Display a welcome message
        welcome_message = (
            f"Welcome to the Automated {business_name} Report Service!\n\n"
            "Any changes made to the code require updating the service, "
            "which can be done from the Service menu. Please be patient as updating the service may take some time."
        )

        self.welcome_label = tk.Label(root, text=welcome_message, padx=20, pady=20)
        self.welcome_label.pack()

    def send_email_now(self):
        generate_reports()
        messagebox.showinfo("Email Sent", "Reports have been sent via email.")

    def open_service_manager(self):
        service_manager_window = tk.Toplevel(self.root)
        service_manager_app = ServiceManagerApp(service_manager_window)

    def open_config_editor(self):
        # Launch the PyQt5-based configuration editor in a separate process
        subprocess.Popen(["python", "configeditor_qt.py"])

    def open_code_file(self, code_base_directory, file_name):
        # Launch the PyQt5-based code editor for the selected code file
        code_file_path = os.path.join(code_base_directory, file_name)
        subprocess.Popen(["python", "codeeditor_qt.py", code_file_path])

    def call_rebuild_app(self):
    # Call the rebuild_app function and pass self as an argument
        rebuild_app(self)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
