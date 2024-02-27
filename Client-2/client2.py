import socket
import threading


# Function to receive messages from the server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            print(message)
        except OSError:  # Client disconnected
            break


# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect(('127.0.0.1', 9999))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

# Send messages to the server
while True:
    message = input()
    client.send(message.encode("utf-8"))
