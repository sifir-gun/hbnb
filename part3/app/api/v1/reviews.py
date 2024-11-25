"""
API Endpoints to manage reviews.
Provides routes to create, retrieve, update, and delete reviews via the API.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade, ValidationError

# Create a namespace for review-related operations
api = Namespace('reviews', description='Review operations')

# Define the data model for reviews
review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description='Text of the review',
        example="Great place to stay!"
    ),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)',
        min=1,
        max=5,
        example=5
    ),
    'place_id': fields.String(
        required=True,
        description='ID of the place being reviewed'
    )
})

facade = HBnBFacade()


@api.route('/')
class ReviewList(Resource):
    """Manage the list of reviews."""

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Cannot review your own place')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """
        Create a new review.
        Protected endpoint - requires authentication.
        Users cannot review their own places or review a place multiple times.
        """
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user['id']

        print("\n=== Creating Review ===")
        print(f"Review data: {review_data}")

        try:
            # Check if the place exists
            place = facade.get_place(review_data['place_id'])
            print(f"Place found: {place is not None}")

            if not place:
                return {'error': 'Place not found'}, 404

            print(f"Place owner: {place.owner_id}")
            print(f"Current user: {current_user['id']}")

            # Check if user owns the place
            if place.owner_id == current_user['id']:
                return {'error': 'You cannot review your own place'}, 400

            # Check for existing review
            existing_review = facade.get_user_review_for_place(
                current_user['id'], review_data['place_id'])
            if existing_review:
                return {'error': 'You have already reviewed this place'}, 400

            # Create the review
            review = facade.create_review(review_data)
            print(f"Review created: {review.id}")

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 201

        except ValidationError as e:
            print(f"Validation error: {str(e)}")
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews."""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Manage individual reviews."""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve review details."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update a review."""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_review = facade.update_review(review_id, api.payload)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
            }, 200
        except ValidationError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review."""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Review not found'}, 404


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Manage reviews for a specific place."""

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a place."""
        # Use facade.get_place instead of facade.place_repo.get
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        } for review in reviews], 200
