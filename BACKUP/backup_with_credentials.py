import tkinter as tk
from tkinter import messagebox, filedialog
import os
import paramiko

def read_credentials():
    try:
        with open("/home/code/map/feb 21:54/mar 12/credentials.txt", "r") as file:
            return file.readline().strip().split(":")
    except FileNotFoundError:
        messagebox.showerror("Error", "Credentials file not found.")
        return None, None

def backup_files_to_server():
    source_dir = source_dir_entry.get()
    server_address = server_address_entry.get()
    server_username = server_username_entry.get()
    server_password = server_password_entry.get()
    server_directory = server_directory_entry.get()

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_address, username=server_username, password=server_password)

    # Create SFTP client
    sftp = ssh.open_sftp()

    try:
        # Change directory to the target directory on the server
        sftp.chdir(server_directory)
    except FileNotFoundError:
        # Create directory if it doesn't exist
        sftp.mkdir(server_directory)
        sftp.chdir(server_directory)

    # Iterate over files in source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            remote_path = os.path.join(server_directory, os.path.relpath(local_path, source_dir))

            # Transfer file to server
            sftp.put(local_path, remote_path)
            status_label.config(text=f"Uploaded {local_path} to {server_address}:{remote_path}")

    # Close connections
    sftp.close()
    ssh.close()

def login():
    stored_username, stored_password = read_credentials()
    if not stored_username or not stored_password:
        return

    username = username_entry.get()
    password = password_entry.get()

    if username == stored_username and password == stored_password:
        
        username_entry.delete(0, tk.END)  # Clear the username entry field
        password_entry.delete(0, tk.END)  # Clear the password entry field
        login_window.withdraw()  # Hide the login window
        create_backup_window()   # Show the backup window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def create_backup_window():
    def logout():
        backup_window.withdraw()
        login_window.deiconify()

    backup_window = tk.Toplevel()
    backup_window.title("File Backup to Server")

    # GUI setup
    source_dir_label = tk.Label(backup_window, text="Source Directory:")
    source_dir_label.grid(row=0, column=0, sticky="e")
    source_dir_entry = tk.Entry(backup_window)
    source_dir_entry.grid(row=0, column=1, padx=5, pady=5)
    source_dir_button = tk.Button(backup_window, text="Browse", command=lambda: source_dir_entry.insert(tk.END, filedialog.askdirectory()))
    source_dir_button.grid(row=0, column=2, padx=5, pady=5)

    server_address_label = tk.Label(backup_window, text="Server Address:")
    server_address_label.grid(row=1, column=0, sticky="e")
    server_address_entry = tk.Entry(backup_window)
    server_address_entry.grid(row=1, column=1, padx=5, pady=5)

    server_username_label = tk.Label(backup_window, text="Username:")
    server_username_label.grid(row=2, column=0, sticky="e")
    server_username_entry = tk.Entry(backup_window)
    server_username_entry.grid(row=2, column=1, padx=5, pady=5)

    server_password_label = tk.Label(backup_window, text="Password:")
    server_password_label.grid(row=3, column=0, sticky="e")
    server_password_entry = tk.Entry(backup_window, show="*")
    server_password_entry.grid(row=3, column=1, padx=5, pady=5)

    server_directory_label = tk.Label(backup_window, text="Server Directory:")
    server_directory_label.grid(row=4, column=0, sticky="e")
    server_directory_entry = tk.Entry(backup_window)
    server_directory_entry.insert(0, "Path Already ")
    server_directory_entry.grid(row=4, column=1, padx=5, pady=5)

    backup_button = tk.Button(backup_window, text="Backup Files", command=backup_files_to_server)
    backup_button.grid(row=5, column=0, columnspan=2, pady=10)

    status_label = tk.Label(backup_window, text="")
    status_label.grid(row=6, column=0, columnspan=2)
    
    logout_button = tk.Button(backup_window, text="Logout", command=logout)
    logout_button.grid(row=7, column=0, columnspan=2, pady=10)

    backup_window.mainloop()

# Create the main application window (login window)
login_window = tk.Tk()
login_window.title("Login")

# Create username label and entry
username_label = tk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Create password label and entry
password_label = tk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Create login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()
