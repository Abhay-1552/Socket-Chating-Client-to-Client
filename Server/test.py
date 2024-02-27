import tkinter as tk
from tkinter import ttk
from tkinter import Text
from datetime import datetime

server_start_time = None


def start_server():
    global server_start_time
    server_start_time = datetime.now()
    status_label.config(text="Server Status: Running", foreground="green")


def stop_server():
    global server_start_time
    if server_start_time:
        stop_time = datetime.now()
        duration = stop_time - server_start_time
        duration_str = str(duration)
        server_time_text.insert(tk.END, f"Server was started at: {server_start_time}\n")
        server_time_text.insert(tk.END, f"Server was stopped at: {stop_time}\n")
        server_time_text.insert(tk.END, f"Duration: {duration_str}\n\n")
    else:
        server_time_text.insert(tk.END, "Server hasn't been started yet.\n")
    status_label.config(text="Server Status: Stopped", foreground="red")


# Create main window
root = tk.Tk()
root.title("Server Control")
root.geometry("500x500")  # Set window size

# Create heading label
heading_label = ttk.Label(root, text="Server Control Panel", font=("Helvetica", 20))
heading_label.pack(pady=20)

# Create frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

# Create start button
start_button = ttk.Button(button_frame, text="Start Server", command=start_server)
start_button.grid(row=0, column=0, padx=5)

# Create stop button
stop_button = ttk.Button(button_frame, text="Stop Server", command=stop_server)
stop_button.grid(row=0, column=1, padx=5)

# Create status label
status_label = ttk.Label(root, text="Server Status: Stopped", foreground="red")
status_label.pack()

# Create text area to display server start and stop times
server_time_text = Text(root, height=10, width=60)
server_time_text.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
