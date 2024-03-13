import socket
import json
import pickle
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Client:
    def __init__(self, encryption_key):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher_suite = Fernet(encryption_key)

    def encrypt_data(self, data):
        # Encrypt data
        return self.cipher_suite.encrypt(data)

    def serialize_data(self, data, format_type='json'):
        # Serialize data based on the format type
        if format_type == 'json':
            return json.dumps(data).encode()
        elif format_type == 'binary':
            return pickle.dumps(data)
        elif format_type == 'xml':
            root = ET.Element("root")
            ET.SubElement(root, "content").text = str(data)
            return ET.tostring(root)
        else:
            raise ValueError("Unsupported serialization format.")

    def connect(self, host, port):
        # Connect to the server
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            print(f"Error connecting to the server: {e}")
            raise e

    def send_data(self, data, format_type='json', encrypt=False):
        # Prepare data
        serialized_data = self.serialize_data(data, format_type)
        if encrypt:
            serialized_data = self.encrypt_data(serialized_data)

        try:
            # Send format type and encryption flag
            self.sock.sendall(f"{format_type},{encrypt}".encode())
            # Send data
            self.sock.sendall(serialized_data)
        except socket.error as e:
            print(f"Error sending data: {e}")
            raise e

if __name__ == "__main__":
    encryption_key = b'Co-BF0ODIcKopN9XnfMXzIaGyb5eyEUVH13NdaEDKS4='  # Same key as the server
    client = Client(encryption_key)

    try:
        # User input for data type, format, and encryption choice
        data_type = input("Send a dictionary or text file? (dict/text): ").lower()
        format_type = input("Choose serialization format (binary, json, xml): ").lower()
        encrypt = input("Encrypt data? (yes/no): ").lower() == 'yes'

        # Prepare data based on user choice
        if data_type == 'dict':
            data = {"message": "Hello, Server!"}  # Example dictionary
        elif data_type == 'text':
            filename = input("Enter the filename: ")
            try:
                with open(filename, "r") as file:
                    data = file.read()  # Read text file content
            except FileNotFoundError as e:
                print(f"File not found: {e}")
                raise e
        else:
            raise ValueError("Unsupported data type.")

        client.connect('localhost', 9999)
        client.send_data(data, format_type, encrypt)
        print("Data sent.")
    except Exception as e:
        print(f"An error occurred: {e}")
