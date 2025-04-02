import os
import json
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess  # Open config file
from cytomine import Cytomine
from cytomine.models import Project, StorageCollection

# Configuration file path
CONFIG_FILE = "config.json"

# Supported image formats
SUPPORTED_FORMATS = (".svs", ".tiff", ".tif", ".ndpi", ".jpg", ".png", ".jpeg", ".zip")

# Load settings from config file
def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

# Save settings to config file
def save_settings():
    config_data = {
        "host": host_entry.get().strip(),
        "upload_host": upload_host_entry.get().strip(),
        "public_key": public_key_entry.get().strip(),
        "private_key": private_key_entry.get().strip(),
        "project_id": project_entry.get().strip(),
        "directory_path": dir_entry.get().strip()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

# Open config file
def open_config_file():
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("Error", "Config file not found! Save settings first.")
        return
    if os.name == "nt":  # Windows
        subprocess.run(["notepad.exe", CONFIG_FILE])
    else:  # Linux/macOS
        subprocess.run(["xdg-open", CONFIG_FILE])

# Select directory
def select_directory():
    folder_path = filedialog.askdirectory()
    if folder_path:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, folder_path)

# Append messages to debug console
def log_message(message):
    debug_console.insert(tk.END, message + "\n")
    debug_console.see(tk.END)  # Auto-scroll

# Upload all images in the selected directory
def upload_images():
    host = host_entry.get().strip()
    upload_host = upload_host_entry.get().strip()
    public_key = public_key_entry.get().strip()
    private_key = private_key_entry.get().strip()
    project_id = project_entry.get().strip()
    directory = dir_entry.get().strip()

    if not host or not upload_host or not public_key or not private_key or not project_id or not directory:
        messagebox.showerror("Error", "Please fill in all fields and select a directory.")
        return

    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Selected directory does not exist. Please check the path.")
        return

    save_settings()  # Save settings before uploading

    try:
        log_message("🔄 Connecting to Cytomine...")
        with Cytomine(host, public_key, private_key) as cytomine:
            # Check if project exists
            project = Project().fetch(int(project_id))
            if not project:
                messagebox.showerror("Error", "Project not found. Please check the Project ID.")
                log_message("❌ Project not found.")
                return

            log_message(f"✅ Connected to Cytomine. Project ID: {project.id}")

            # Fetch available storage
            storages = StorageCollection().fetch()
            my_storage = next((storage for storage in storages if storage.user == cytomine.current_user.id), None)
            if not my_storage:
                messagebox.showerror("Error", "No available storage found for this user.")
                log_message("❌ No available storage found.")
                return

            storage_id = my_storage.id
            log_message(f"✅ Using Storage ID: {storage_id}")

            # Get list of image files
            image_files = [f for f in os.listdir(directory) if f.lower().endswith(SUPPORTED_FORMATS)]
            if not image_files:
                messagebox.showerror("Error", "No valid image files found in the selected directory.")
                log_message("❌ No valid image files found.")
                return

            log_message(f"📂 Found {len(image_files)} images to upload...")

            # Upload each image
            for file in image_files:
                file_path = os.path.join(directory, file)
                log_message(f"📤 Uploading: {file}...")

                try:
                    uploaded_file = cytomine.upload_image(
                        upload_host=upload_host,
                        filename=file_path,
                        id_storage=storage_id,
                        id_project=int(project_id)
                    )

                    if uploaded_file:
                        log_message(f"✅ Uploaded {file} successfully. ID: {uploaded_file.id}")
                    else:
                        log_message(f"❌ Failed to upload {file}.")

                except Exception as e:
                    log_message(f"🚨 Error uploading {file}: {e}")

    except Exception as e:
        log_message(f"🚨 Upload failed. Error: {e}")

# Creating GUI window
root = tk.Tk()
root.title("Cytomine Batch Image Uploader")
root.geometry("750x500")

# Load previous settings
settings = load_settings()

# Labels and Entry Fields
tk.Label(root, text="Cytomine Host:").pack()
host_entry = tk.Entry(root, width=50)
host_entry.pack()
host_entry.insert(0, settings.get("host", ""))

tk.Label(root, text="Upload Host:").pack()
upload_host_entry = tk.Entry(root, width=50)
upload_host_entry.pack()
upload_host_entry.insert(0, settings.get("upload_host", ""))

tk.Label(root, text="Public Key:").pack()
public_key_entry = tk.Entry(root, width=50, show="*")
public_key_entry.pack()
public_key_entry.insert(0, settings.get("public_key", ""))

tk.Label(root, text="Private Key:").pack()
private_key_entry = tk.Entry(root, width=50, show="*")  # Hide private key
private_key_entry.pack()
private_key_entry.insert(0, settings.get("private_key", ""))

tk.Label(root, text="Project ID:").pack()
project_entry = tk.Entry(root, width=50)
project_entry.pack()
project_entry.insert(0, settings.get("project_id", ""))

tk.Label(root, text="Select Directory:").pack()
dir_entry = tk.Entry(root, width=40)
dir_entry.pack(side=tk.LEFT, padx=5)
dir_entry.insert(0, settings.get("directory_path", ""))
tk.Button(root, text="Browse", command=select_directory).pack(side=tk.RIGHT, padx=5)

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Upload Button
upload_button = tk.Button(button_frame, text="Upload", command=upload_images, bg="green", fg="white", width=15)
upload_button.grid(row=0, column=0, padx=5)

# Open Config Button
open_config_button = tk.Button(button_frame, text="Open Config File", command=open_config_file, bg="blue", fg="white", width=15)
open_config_button.grid(row=0, column=1, padx=5)

# Debug Console
debug_console = scrolledtext.ScrolledText(root, width=40, height=20)
debug_console.pack(side=tk.RIGHT, padx=10, pady=10)
debug_console.insert(tk.END, "📌 Debug Console: Logs will appear here...\n")

# Run the GUI
root.mainloop()
