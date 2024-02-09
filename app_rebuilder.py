import subprocess
import os
from datetime import datetime
import shutil
from tkinter import messagebox
import threading
from config import business_name

def rebuild_app(main_app):
    def rebuild_in_background():
        try:
            # Get the current date and time to create a unique name
            now = datetime.now()
            date_string = now.strftime("%Y%m%d")
            new_app_name = f"{business_name}_{date_string}.exe"

            # Get the current working directory
            current_directory = os.getcwd()

            script_filename = "gui.py"

            # Create the full path to the script using os.path.join
            script_path = os.path.join(current_directory, script_filename)

            # Define the destination directory for the executable
            dst_exe_path = os.getcwd()

            # Check for and delete the "dist" folder if it exists
            dist_folder = os.path.join(dst_exe_path, "dist")
            if os.path.exists(dist_folder):
                shutil.rmtree(dist_folder)

            # Check for and delete existing executable (.exe) and spec (.spec) files in dst_exe_path
            for filename in os.listdir(dst_exe_path):
                if filename.endswith(".exe") or filename.endswith(".spec"):
                    file_path = os.path.join(dst_exe_path, filename)
                    os.remove(file_path)

            # Rebuild the app with the new name using PyInstaller or your packaging tool
            # Adjust the PyInstaller command as needed
            process = subprocess.Popen(["py", "-m", "PyInstaller", "--name", new_app_name, "--onefile", script_path])

            # Wait for the process to complete
            process.wait()

            # Move the new executable to the root folder (assuming 'dist' is the build output folder)
            src_exe_path = os.path.join("dist", new_app_name)
            src_exe_path = os.path.join(os.getcwd(), src_exe_path)
            dst_exe_path = os.path.join(os.getcwd(), new_app_name)
            shutil.copy(src_exe_path, dst_exe_path)        

            # Display a message box with information about the new app and old app
            message = (
                f"The rebuilt application can be found at:\n{dst_exe_path}\n\n"
                f"You can delete the old application"
            )
            messagebox.showinfo("App Rebuilt", message)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Create a new thread to run the rebuild_in_background function
    rebuild_thread = threading.Thread(target=rebuild_in_background)
    
    # Start the thread
    rebuild_thread.start()
