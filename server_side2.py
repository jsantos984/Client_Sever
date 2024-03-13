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
        try:
            return self.cipher_suite.decrypt(encrypted_data)
        except Fernet.InvalidToken as e:
            print("Invalid decryption token or key.", e)
            return None

    def deserialize_data(self, data, format_type):
        try:
            if format_type == 'json':
                return json.loads(data)
            elif format_type == 'binary':
                return pickle.loads(data)
            elif format_type == 'xml':
                return ET.fromstring(data).find('content').text
            else:
                raise ValueError("Unsupported serialization format.")
        except (json.JSONDecodeError, pickle.UnpicklingError, ET.ParseError, ValueError) as e:
            print(f"Deserialization error: {e}")
            return None

    def bind_and_listen(self, host, port):
        try:
            self.sock.bind((host, port))
            self.sock.listen()
            print(f"Server listening on {host}:{port}")
        except socket.error as e:
            print(f"Socket error: {e}")
            raise e

    def accept_connection(self):
        try:
            return self.sock.accept()
        except socket.error as e:
            print(f"Error accepting connections: {e}")
            return None, None

    def receive_and_process_data(self, conn):
        try:
            header = conn.recv(1024).decode()
            format_type, encrypted = header.split(',')
            encrypted = encrypted == 'True'

            data = b''
            while True:
                packet = conn.recv(4096)
                if not packet: break
                data += packet

            if encrypted:
                data = self.decrypt_data(data)
                if data is None:
                    return

            deserialized_data = self.deserialize_data(data, format_type)
            if deserialized_data is not None:
                print("Received data:", deserialized_data)
        except socket.error as e:
            print(f"Error receiving data: {e}")
        finally:
            conn.close()

    def run(self):
        try:
            print("Server is running...")
            while True:
                conn, addr = self.accept_connection()
                if conn and addr:
                    print(f"Connection accepted from {addr}")
                    self.receive_and_process_data(conn)
        finally:
            self.sock.close()

if __name__ == "__main__":
    encryption_key = b'Co-BF0ODIcKopN9XnfMXzIaGyb5eyEUVH13NdaEDKS4='  # Must match the client's key
    server = Server(encryption_key)
    try:
        server.bind_and_listen('localhost', 9999)
        server.run()
    except Exception as e:
        print(f"An error occurred: {e}")
