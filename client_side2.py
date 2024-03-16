import socket
import json
import pickle
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Client:
    def __init__(self, encryption_key):
        #Initialize socket and encryption components
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cipher_suite = Fernet(encryption_key)

    def encrypt_data(self, data):
        # Encrypt data using Fernet symmetric encryption
        return self.cipher_suite.encrypt(data)

    def serialize_data(self, data, format_type='json'):
        # Serialize data based on the format type provided (json, binary, or xml)
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
        # Connect to the server using the provided host and port
        self.sock.connect((host, port))

    def send_data(self, data, format_type='json', encrypt=False):
        # Prepare data - Serialize the data and then check if encryption is required
        serialized_data = self.serialize_data(data, format_type)
        if encrypt:
            serialized_data = self.encrypt_data(serialized_data)

        # Send format type and encryption flag to the server
        self.sock.send(f"{format_type},{encrypt}".encode())
        # Send actual data
        self.sock.send(serialized_data)

if __name__ == "__main__":
    # The encryption key should be the same as used by the server for successful decryption
    encryption_key = b'Co-BF0ODIcKopN9XnfMXzIaGyb5eyEUVH13NdaEDKS4='
    client = Client(encryption_key)

    # User input for data type, format, and encryption choice
    data_type = input("Send a dictionary or text file? (dict/text): ").lower()
    format_type = input("Choose serialization format (binary, json, xml): ").lower()
    encrypt = input("Encrypt data? (yes/no): ").lower() == 'yes'

    # Prepare data based on user choice
    if data_type == 'dict':
        # Example dictionary data is created and populated here
        data = {"message": "Hello, Server!"}
    elif data_type == 'text':
        # The client reads from a text file (considers adding functionality to create a text file if it does not exist)
        filename = input("Enter the filename: ")
        with open(filename, "r") as file:
            data = file.read()  # Read text file content
    else:
        raise ValueError("Unsupported data type.")  # Return error message

    # Connect to the server (please use the correct host and port for the server)
    client.connect('localhost', 9999)
    # Send the data after serialization and optional encryption
    client.send_data(data, format_type, encrypt)
    print("Data sent.") # Confirm to the user that data has been sent
