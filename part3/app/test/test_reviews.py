import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        # Set up the app and test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True  # Set testing mode

    def test_create_review(self):
        # Test creating a valid review
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": "123",  # Assume user exists for test
            "place_id": "456"  # Assume place exists for test
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review successfully created',
                      response.get_json().get('message', ''))

    def test_create_review_invalid_data(self):
        # Test creating a review with invalid data
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,  # Invalid rating (should be between 1-5)
            "user_id": "123",
            "place_id": "456"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input data', response.get_json()['error'])

    def test_get_reviews(self):
        # Test retrieving all reviews
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_review_by_id(self):
        # Test retrieving a review by a specific ID
        review_id = "1"  # Assume this review exists for the test
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.get_json())

    def test_get_nonexistent_review(self):
        # Test retrieving a review that doesn't exist
        review_id = "9999"  # Assume this review does not exist
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['error'])


if __name__ == '__main__':
    unittest.main()
