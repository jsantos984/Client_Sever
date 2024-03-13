# Client_Sever
Sw development Module Final Exercise - CSCK541

Overview
This application is a client-server communication model. The client can serialize data in various formats 
(JSON, binary, XML), optionally encrypt it, and then send it to the server. The server receives, decrypts (if necessary),
and deserializes the data for processing.



Requirements
To run this application, you will need Python 3.x installed. You also need to install required dependencies:

- pip install -r requirements.txt

- Setting Up
Encryption Key: Ensure you have a valid Fernet key. If you need to generate a new key, use:
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()

Running the Application
1. Start the Server: Run server.py first to start listening for incoming connections.
- python server.py

2. Run the Client: Execute client.py to start the client application.
- python client.py

Testing
1. Run unit tests for both client and server:
- python test_client.py
- python test_server.py
