import socket
import json
import pickle
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Server:
    def __init__(self, encryption_key):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher_suite = Fernet(encryption_key)
    
    def decrypt_data(self, encrypted_data):
        # Decrypt data; if there's an error, return None
        try:
            return self.cipher_suite.decrypt(encrypted_data)
        except cryptography.fernet.InvalidToken:
            print("Invalid decryption token or key.")
            return None

    def deserialize_data(self, data, format_type):
        # Deserialize data based on the format type
        if format_type == 'json':
            return json.loads(data)
        elif format_type == 'binary':
            return pickle.loads(data)
        elif format_type == 'xml':
            # For XML, extracting the content under a 'content' tag
            return ET.fromstring(data).find('content').text
        else:
            print("Unsupported format type.")
            return None

    def bind_and_listen(self, host, port):
        # Bind the server to a specified host and port, then listen for connections
        self.sock.bind((host, port))
        self.sock.listen()
        print(f"Server listening on {host}:{port}")

    def accept_connection(self):
        # Accept an incoming connection
        return self.sock.accept()

    def receive_and_process_data(self, conn):
        # Receive data from the client
        try:
            # Assuming the format and encryption flag are sent first
            format_type, encrypted = conn.recv(1024).decode().split(',')
            data = conn.recv(4096)  # Adjust buffer size based on your data needs

            if encrypted == 'True':
                data = self.decrypt_data(data)
                if data is None:  # Failed decryption
                    return

            # Deserialize data based on format type
            deserialized_data = self.deserialize_data(data, format_type)
            print("Received data:", deserialized_data)
        finally:
            conn.close()

    def run(self):
        print("Server is running...")
        while True:
            conn, addr = self.accept_connection()
            print(f"Connection accepted from {addr}")
            self.receive_and_process_data(conn)

if __name__ == "__main__":
    encryption_key = b'Co-BF0ODIcKopN9XnfMXzIaGyb5eyEUVH13NdaEDKS4='  # Your Fernet key
    server = Server(encryption_key)
    server.bind_and_listen('localhost', 9999)
    server.run()
