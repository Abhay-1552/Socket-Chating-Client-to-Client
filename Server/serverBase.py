import socket
from _thread import start_new_thread
import tkinter as tk
from tkinter import ttk
from tkinter import Text
from datetime import datetime


class Server:
    def __init__(self):
        super().__init__()

        self.server_start_time = None
        self.running_server = None

        # Declaring server variables
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 8000)
        self.thread_count = 0

        # Tkinter Framework
        self.root = tk.Tk()
        self.root.title("Server Control")
        self.root.geometry("500x500")

        self.heading_label = ttk.Label(self.root, text="Server Control Panel", font=("Helvetica", 20))
        self.heading_label.pack(pady=20)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.start_button = ttk.Button(self.button_frame, text="Start Server", command=self.start_server)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(self.button_frame, text="Stop Server", command=self.stop_server)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.status_label = ttk.Label(self.root, text="Server Status: Stopped", foreground="red")
        self.status_label.pack()

        self.server_time_text = Text(self.root, height=10, width=60)
        self.server_time_text.pack(pady=20)

        self.active_connections = ttk.Label(self.root, text="Active Connections", foreground="dark blue")
        self.active_connections.pack(pady=5)

        self.thread_count_text = Text(self.root, height=8, width=60)
        self.thread_count_text.pack(pady=5)

        self.root.mainloop()

    def start_server(self):
        self.server_start_time = datetime.now()
        self.status_label.config(text="Server Status: Running", foreground="green")
        self.server_time_text.insert(tk.END, f"Server started at: {self.server_start_time}\n")

        try:
            self.server_socket.bind(self.server_address)
        except socket.error as e:
            print(f"Error: {e}")
            return

        self.server_socket.listen(5)
        self.running_server = True

        start_new_thread(self.accept_clients, ())

    def accept_clients(self):
        while self.running_server:
            try:
                client, addr = self.server_socket.accept()
                self.thread_count_text.insert(tk.END, f"Connected to {addr}\n")

                start_new_thread(self.client_thread, (client, addr))

                self.thread_count += 1
                self.thread_count_text.insert(tk.END, f"Thread Count: {self.thread_count}\n")

            except OSError:
                break

    def client_thread(self, connection, addr):
        connection.send(str.encode("Welcome to Server\n"))

        while True:
            try:
                data = connection.recv(2048)

                if not data:
                    break

                decoded_data = data.decode('utf-8')

                reply = f"From {addr} - " + data.decode('utf-8')
                connection.sendall(str.encode(reply))

                # connection.sendall(str.encode(decoded_data))
                print(f"Received data from {addr}: {decoded_data}")

            except ConnectionResetError:
                break

        connection.close()
        self.thread_count -= 1
        self.thread_count_text.insert(tk.END, f"Disconnected to {addr}\n")
        self.thread_count_text.insert(tk.END, f"Thread Count: {self.thread_count}\n")

    def stop_server(self):
        try:
            self.server_socket.close()
        except NameError:
            self.server_time_text.insert(tk.END, "Server socket not defined.\n")

        if self.server_start_time:
            stop_time = datetime.now()
            duration = str(stop_time - self.server_start_time)
            self.server_time_text.insert(tk.END, f"Server stopped at: {stop_time}\n")
            self.server_time_text.insert(tk.END, f"Duration: {duration}\n\n")
        else:
            self.server_time_text.insert(tk.END, "Server hasn't been started yet.\n")

        self.status_label.config(text="Server Status: Stopped", foreground="red")


if __name__ == '__main__':
    Server()
