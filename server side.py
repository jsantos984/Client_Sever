import socket
import json
import pickle
from cryptography.fernet import Fernet

# Generate a key for Fernet
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)
print(f"Encryption Key: {encryption_key.decode()}")

def decrypt_data(data):
    return cipher_suite.decrypt(data).decode()

def deserialize_data(data, format_type):
    if format_type == 'json':
        return json.loads(data)
    elif format_type == 'binary':
        return pickle.loads(data)
    else:
        raise ValueError('Unsupported format type')

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server is listening...")
        
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            # First, receive the format type and encryption flag
            format_type, encrypted = conn.recv(1024).decode().split(',')
            
            # Then, receive the actual data
            data = conn.recv(1024)
            if encrypted == 'True':
                data = decrypt_data(data)
                
            deserialized_data = deserialize_data(data, format_type)
            print("Received Data:", deserialized_data)

if __name__ == "__main__":
    start_server()
