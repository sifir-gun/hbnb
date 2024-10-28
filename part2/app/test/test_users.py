
import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        # Set up the app and test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True  # Set the testing flag to True

    def test_create_user(self):
        # Test creating a valid user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

        # Extract JSON response and check for fields
        response_json = response.get_json()
        self.assertIn('id', response_json)  # Check if user ID is present
        self.assertEqual(response_json['first_name'], 'Jane')
        self.assertEqual(response_json['last_name'], 'Doe')
        self.assertEqual(response_json['email'], 'jane.doe@example.com')

    def test_create_user_invalid_data(self):
        # Test creating a user with invalid email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "ValidFirstName",
            "last_name": "ValidLastName",
            "email": "invalid-email"  # Invalid email format
        })
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()

        # Check if 'error' is in the response and the message is correct
        self.assertIn('error', response_json)
        self.assertIn('A valid email address is required.',
                      response_json['error'])

    def test_create_user_empty_first_name(self):
        # Test creating a user with an empty first name
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",  # Invalid first name
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()

        # Check for the appropriate error message for first name
        self.assertIn('error', response_json)
        self.assertIn(
            'First Name is required and must be at most 50 characters long.', response_json['error'])

    def test_create_user_duplicate_email(self):
        # Test creating a user with a duplicate email (email already exists)
        # First create a valid user
        self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        # Attempt to create another user with the same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "jane.doe@example.com"  # Duplicate email
        })
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()

        # Check for the error message indicating duplicate email
        self.assertIn('error', response_json)
        self.assertIn('The email is already in use by another user.',
                      response_json['error'])


if __name__ == '__main__':
    unittest.main()
