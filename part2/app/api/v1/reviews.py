"""
API Endpoints to manage reviews.
Provides routes to create, retrieve, update, and delete reviews via the API.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade, ValidationError

# Create a namespace for review-related operations
api = Namespace('reviews', description='Review operations')

# Define the data model for a review, used for validation and API documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating of the place (1-5)'
    ),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Initialize HBnB facade to handle business logic
facade = HBnBFacade()


@api.route('/')
class ReviewList(Resource):
    """
    Resource to manage the list of reviews.
    Allows creating a new review (POST) or retrieving all reviews (GET).
    """

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new review.
        
        Returns:
            dict: Details of the created review or error message if validation fails.
        """
        review_data = api.payload
        try:
            review = facade.create_review(review_data)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 201
        except ValidationError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.

        Returns:
            list: A list of reviews with HTTP status 200.
        """
        # Call facade to retrieve all reviews
        reviews = facade.get_all_reviews()
        # Format reviews for the response
        review_list = [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in reviews
        ]
        # Return the list of reviews with HTTP status 200
        return review_list, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource to manage a specific review by its ID.
    Allows retrieving (GET), updating (PUT), or deleting (DELETE) a review.
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Retrieve review details by ID.

        Args:
            review_id (str): ID of the review to retrieve.

        Returns:
            dict: Review details with HTTP status 200 or error message if not found.
        """
        review = facade.get_review(review_id)  # Retrieve review via facade
        if not review:
            # Return error if review does not exist
            return {'error': 'Review not found'}, 404
        # Return review details with HTTP status 200
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """
        Update review information.

        Args:
            review_id (str): ID of the review to update.

        Returns:
            dict: Updated review details with HTTP status 200, error 400 for invalid data,
                  or error 404 if review is not found.
        """
        review_data = api.payload  # Retrieve updated review data
        # Update review via facade
        review = facade.update_review(review_id, review_data)
        if not review:
            # Return error if review does not exist
            return {'error': 'Review not found'}, 404
        # Return updated review details with HTTP status 200
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review by its ID.

        Args:
            review_id (str): ID of the review to delete.

        Returns:
            dict: Confirmation message with HTTP status 200 or error 404 if review is not found.
        """
        success = facade.delete_review(review_id)  # Delete review via facade
        if not success:
            # Return error if review does not exist
            return {'error': 'Review not found'}, 404
        # Return success message with HTTP status 200
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource to manage reviews associated with a specific place.
    Allows retrieving all reviews for a given place by its ID.
    """

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve all reviews associated with a specific place.

        Args:
            place_id (str): ID of the place for which to retrieve reviews.

        Returns:
            list: A list of reviews for the specified place with HTTP status 200 or error 404 if place is not found.
        """
        # Check if the place exists via the facade
        place = facade.place_repo.get(place_id)
        if not place:
            # Return error if place does not exist
            return {'error': 'Place not found'}, 404

        # Retrieve all reviews associated with this place
        reviews = facade.get_reviews_by_place(place_id)
        # Format reviews for the response
        review_list = [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in reviews
        ]
        # Return the list of reviews with HTTP status 200
        return review_list, 200
