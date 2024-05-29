from socket import *
from _thread import *


class Server:
    def __init__(self):
        self.server_socket = socket()

        self.server_address = ('127.0.0.1', 9999)
        self.thread_count = 0

    def start_server(self):
        try:
            self.server_socket.bind(self.server_address)
        except error as e:
            print(f"Error: {e}")

        print("Waiting for Clients Connection!!")
        self.server_socket.listen(5)

        while True:
            client, addr = self.server_socket.accept()
            print(f"Connected to {addr}")

            start_new_thread(self.client_thread, (client, addr))
            self.thread_count += 1
            print(f"Thread Count: {self.thread_count}")

    @staticmethod
    def client_thread(connection, addr):
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

    def close_server(self):
        self.server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start_server()
    server.close_server()
