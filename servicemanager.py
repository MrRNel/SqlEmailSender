# this is the GUI interface to manage the background service
import tkinter as tk
import subprocess
import psutil

class ServiceManagerApp:
    def __init__(self, root):
        self.root = root
        root.title("Service Manager")
        
        # Increase the window size
        root.geometry("400x400")

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Create a frame to contain the widgets for better organization
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Service Status:")
        self.label.pack()

        self.status_label = tk.Label(self.frame, text="Unknown")
        self.status_label.pack()

        # Add padding between buttons
        button_padding = 10

        self.start_button = tk.Button(self.frame, text="Start Service", command=self.start_service)
        self.start_button.pack(pady=button_padding)

        self.stop_button = tk.Button(self.frame, text="Stop Service", command=self.stop_service)
        self.stop_button.pack(pady=button_padding)

        self.restart_button = tk.Button(self.frame, text="Restart Service", command=self.restart_service)
        self.restart_button.pack(pady=button_padding)

        self.update_button = tk.Button(self.frame, text="Update Service", command=self.update_service)
        self.update_button.pack(pady=button_padding)

        self.refresh_button = tk.Button(self.frame, text="Refresh Status", command=self.update_status)
        self.refresh_button.pack(pady=button_padding)

        self.update_status()  # Update the initial status
        self.update_button_state()  

    def is_service_running(self):
        myDaemonService = psutil.win_service_get("BoulderEmailService")
        serviceStatus = myDaemonService.as_dict()['status']
        if serviceStatus == 'stopped':
            return False
        else:
            return True

    def update_status(self):
        if self.is_service_running():
            self.status_label.config(text="Running")
        else:
            self.status_label.config(text="Stopped")

    def update_button_state(self):
        is_running = self.is_service_running()
        self.start_button.config(state="normal" if not is_running else "disabled")
        self.stop_button.config(state="normal" if is_running else "disabled")
        self.restart_button.config(state="normal" if is_running else "disabled")
        self.update_button.config(state="normal" if not is_running else "disabled")

    def start_service(self):
        subprocess.run(["python", "backgroundService.py", "start"])
        self.update_status()
        self.update_button_state()

    def stop_service(self):
        subprocess.run(["python", "backgroundService.py", "stop"])
        self.update_status()
        self.update_button_state()

    def restart_service(self):
        subprocess.run(["python", "backgroundService.py", "restart"])
        self.update_status()
        self.update_button_state()

    def update_service(self):
        subprocess.run(["python", "backgroundService.py", "stop"])
        subprocess.run(["python", "backgroundService.py", "install"])
        subprocess.run(["python", "backgroundService.py", "start"])
        self.update_status()
        self.update_button_state()
