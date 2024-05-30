import socket
from socket import error
from _thread import start_new_thread
import tkinter as tk
from tkinter import ttk
from tkinter import Text
from datetime import datetime

server_start_time: datetime | None = None

class Server:
    def __init__(self):
        super().__init__()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_address = ('127.0.0.1', 9999)
        self.thread_count = 0

        # Tkinter Frame
        self.root = tk.Tk()
        self.root.title("Server Control")
        self.root.geometry("500x500")  # Set window size

        # Create heading label
        self.heading_label = ttk.Label(self.root, text="Server Control Panel", font=("Helvetica", 20))
        self.heading_label.pack(pady=20)

        # Create frame for buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=20)

        # Create start button
        self.start_button = ttk.Button(self.button_frame, text="Start Server", command=self.start_server)
        self.start_button.grid(row=0, column=0, padx=5)

        # Create stop button
        self.stop_button = ttk.Button(self.button_frame, text="Stop Server", command=self.stop_server)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Create status label
        self.status_label = ttk.Label(self.root, text="Server Status: Stopped", foreground="red")
        self.status_label.pack()

        # Create text area to display server start and stop times
        self.server_time_text = Text(self.root, height=10, width=60)
        self.server_time_text.pack(pady=20)

        # Run the Tkinter event loop
        self.root.mainloop()

    def start_server(self) -> None:
        global server_start_time

        server_start_time = datetime.now()
        self.status_label.config(text="Server Status: Running", foreground="green")
        self.server_time_text.insert(tk.END, f"Server was started at: {server_start_time}\n")

        try:
            self.server_socket.bind(self.server_address)
        except error as e:
            print(f"Error: {e}")
            return

        print("Waiting for Clients Connection!!")
        self.server_socket.listen(5)

        start_new_thread(self.accept_clients, ())

    def accept_clients(self) -> None:
        while True:
            client, addr = self.server_socket.accept()
            print(f"Connected to {addr}")

            start_new_thread(self.client_thread, (client, addr))
            self.thread_count += 1
            print(f"Thread Count: {self.thread_count}")

    def client_thread(self, connection: socket.socket, addr: tuple[str, int]) -> None:
        connection.send(str.encode("Welcome to Server"))

        while True:
            try:
                data = connection.recv(2048)

                if not data:
                    break

                reply = "Hello I am Server - " + data.decode('utf-8')
                connection.sendall(str.encode(reply))

                decoded_data = data.decode('utf-8')
                print(f"Received data from {addr}: {decoded_data}")

            except ConnectionResetError:
                print(f"Connection with {addr} was forcibly closed by the remote host")
                break

        connection.close()

        self.thread_count -= 1
        print(f"Thread Count: {self.thread_count}")

    def stop_server(self):
        global server_start_time

        try:
            self.server_socket.close()
        except NameError:
            self.server_time_text.insert(tk.END, "Server socket not defined.\n")

        if server_start_time:
            stop_time = datetime.now()
            duration: str = str(stop_time - server_start_time)

            self.server_time_text.insert(tk.END, f"Server was stopped at: {stop_time}\n")
            self.server_time_text.insert(tk.END, f"Duration: {duration}\n\n")
        else:
            self.server_time_text.insert(tk.END, "Server hasn't been started yet.\n")

        self.status_label.config(text="Server Status: Stopped", foreground="red")


if __name__ == '__main__':
    Server()
