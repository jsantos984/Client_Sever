The following readme file summarises the client-to-server communication created as part of the group project for the summative assessment of CSCK541 Software Development in Practice January 2024 C.

### ***Index***


* Getting started
* Tools requirements and installation
* Development
* Authors


###  **Geetting started**

The aim of the project is to utilise Python programming to implement client-server connections (Figure 1) and convey different forms of data through different encryption methods


![Screenshot 2024-03-15 alle 09 41 10](https://github.com/jsantos984/Client_Sever/assets/158838122/b14e51cd-9163-466c-a5e1-0d92f95ce71d)


###  ***Tools requirements and installation***
 
For the purpose of this program, no specific tools are necessary. The program can be used in IDLE and other terminals that support Python language.

To access the file, please use the following path.

	└──github.com/
		└── jsantos985/
    		└── Client_Server/
   

### **Development**

The project's development was carried out on two main files (i.e., client_skeleton and server_skeleton). Following the creation of the main codes, tests were carried out (refer to client_test and server_test).

The application architecture consists of two main components: a server and a client. The server listens for incoming connections, receives data, decrypts and deserialises it, and then processes it as required. The client, on the other hand, serialises, encrypts, and sends data to the server. This bidirectional communication is facilitated using TCP/IP sockets, providing a reliable stream of bytes between the client and server (Yadav, 2007).

Server-Side Implementation
The server is initiated with a cryptographic key, setting up a Fernet cypher suite for decryption purposes (Wijaya et al., 2022). It creates a TCP socket using socket.socket(socket.AF_INET, socket.SOCK_STREAM), binds to a host and port, and then listens for incoming connections. Upon accepting a connection, it reads data sent by the client. If the data is encrypted, the server attempts decryption using the provided key. The code also handles errors in connection, encryption, key, and serialization. Data deserialisation is flexible, supporting JSON, binary (via Python's pickle), and XML formats. This versatility allows the server to handle a variety of data types and structures, enhancing the application's adaptability to different use cases. Deserialisation errors or unsupported formats result in appropriate error handling or messages

Client-Side Implementation
Similarly, the client is initialised with the same cryptographic key for encryption, ensuring secure data transmission (Hidayat and Mahardiko, 2020). The client's main functionality includes data serialisation and encryption. Supported serialisation formats are JSON, binary, and XML, mirroring the server's capabilities. This ensures that any data sent by the client can be appropriately understood and processed by the server 
The client encrypts serialised data before sending it over the network, ensuring that data confidentiality is maintained during transmission. The encryption and decryption process relies on a shared secret key, using symmetric encryption provided by the Fernet module from the cryptography library, which is known for its ease of use and security.


### **Authors**

Joao Pedro Santos --> Project manager

Jacopo Saraiva --> Software Tester 		  

Francesco V Ferraro --> Software Architect

Moustafa Said Hassan Foud --> Software Engineer

