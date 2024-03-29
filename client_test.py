import unittest
from client_side2 import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        # Set up the Client instance with a known encryption key for testing
        self.encryption_key = b'Co-BF0ODIcKopN9XnfMXzIaGyb5eyEUVH13NdaEDKS4='
        self.client = Client(self.encryption_key)

    def tearDown(self):
        # Close the socket after each test
        if self.client.sock.fileno() != -1:
            self.client.sock.close()

    def test_encrypt_data(self):
        # Test encryption of data
        data = b'TestData'
        encrypted_data = self.client.encrypt_data(data)
        self.assertNotEqual(data, encrypted_data)

    def test_serialize_data_json(self):
        # Test JSON serialization
        data = {"message": "Hello, Server!"}
        serialized_data = self.client.serialize_data(data, format_type='json')
        self.assertEqual(serialized_data, b'{"message": "Hello, Server!"}')

    def test_serialize_data_binary(self):
        # Test binary serialization
        data = {"message": "Hello, Server!"}
        serialized_data = self.client.serialize_data(data, format_type='binary')
        self.assertIsNotNone(serialized_data)

    def test_serialize_data_xml(self):
        # Test XML serialization
        data = {"message": "Hello, Server!"}
        serialized_data = self.client.serialize_data(data, format_type='xml')
        self.assertIsNotNone(serialized_data)

    def test_unsupported_data_type(self):
        # Test error handling for unsupported data type
        invalid_data_type = 'unsupported_type'
        data = {"message": "Hello, Server!"}

        # Connect the client before sending data
        self.client.connect('localhost', 9999)

        with self.assertRaises(ValueError) as context:
            # Attempt to send data with an unsupported serialization format
            self.client.send_data(data, format_type=invalid_data_type, encrypt=False)

        self.assertEqual(
            str(context.exception),
            "Unsupported serialization format."
        )


if __name__ == '__main__':
    unittest.main()

