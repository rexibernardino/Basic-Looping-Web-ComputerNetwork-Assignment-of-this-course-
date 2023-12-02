import socket

class FileClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")

    def request_file(self, file_path):
        try:
            self.client_socket.sendall(file_path.encode('utf-8'))

            response = self.client_socket.recv(1024)
            print(response.decode('utf-8'))

        except ConnectionResetError:
            print("Server connection closed.")

    def close(self):
        if self.client_socket:
            self.client_socket.close()

client = FileClient('localhost', 8000)
client.connect()

while True:
    file_path = input("Enter file path (or 'exit' to quit): ")
    if file_path.lower() == 'exit':
        break
    client.request_file(file_path)

client.close()
