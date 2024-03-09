import socket
import json
import pickle
from cryptography.fernet import Fernet

# Use the same encryption key as printed by the server
encryption_key = b'bxT70Vnmh6p2gJnDwbI_Uq-Q8su1NydqPNBzKjjIUkA='
cipher_suite = Fernet(encryption_key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def serialize_data(data, format_type):
    if format_type == 'json':
        return json.dumps(data).encode()
    elif format_type == 'binary':
        return pickle.dumps(data)
    else:
        raise ValueError('Unsupported format type')

def send_data(host='127.0.0.1', port=65432, data={}, format_type="json", encrypt=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Sending format type and encryption flag
        s.send(f"{format_type},{encrypt}".encode())
        
        serialized_data = serialize_data(data, format_type)
        if encrypt:
            serialized_data = encrypt_data(serialized_data.decode())
        
        s.send(serialized_data)

if __name__ == "__main__":
    # Example dictionary and text from a file (for demonstration, ensure the file exists)
    example_dict = {"message": "Hello, Server!"}
    with open("C:/Users/moust/Downloads/example.txt", "r") as file:
        text_content = file.read()
    
    # Combine dictionary and text file content into one dictionary
    combined_data = {"dict": example_dict, "file_content": text_content}
    send_data(data=combined_data, format_type="json", encrypt=True)
