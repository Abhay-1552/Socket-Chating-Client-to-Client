import socket
import threading


class CLIENT:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 9999))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                print(message)
                return message
            except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"

    def send_messages(self, message):
        self.client.send(message.encode("utf-8"))


# if __name__ == '__main__':
#     client = CLIENT()
#     client.send_messages()