import socket
import threading


# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connected: {client_address}")

    while True:
        # Receive message from client
        message = client_socket.recv(1024).decode("utf-8")
        if not message:
            break

        print(f"Received from {client_address}: {message}")

        # Send the received message to all other clients
        for c in clients:
            if c != client_socket:
                c.send(message.encode("utf-8"))

    # Remove the disconnected client from the list
    clients.remove(client_socket)
    client_socket.close()
    print(f"Disconnected: {client_address}")


# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server.bind(('127.0.0.1', 9999))

# Listen for incoming connections
server.listen(2)  # Maximum 2 clients

print("Server is listening...")

# List to store client sockets
clients = []

while True:
    # Accept a new connection
    client_socket, client_address = server.accept()
    clients.append(client_socket)

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
