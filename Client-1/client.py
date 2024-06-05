import socket
import asyncio


class CLIENT:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 9999))

    async def receive_messages(self):
        while True:
            try:
                message = await asyncio.to_thread(self.client.recv, 1024)
                message = message.decode("utf-8")
                print(message)
                return message

            except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"

    def send_messages(self, message):
        self.client.send(message.encode("utf-8"))
