from flask import Flask
from flask_restx import Api, Resource, fields
from app.services.facade import HBnBFacade


"""Endpoints API pour gérer les reviews (avis)."""
"""Fournit des routes pour créer, modifier, récupérer
 et supprimer des reviews via l'API."""


app = Flask(__name__)
api = Api(app)


facade = None


user_model = api.model('User', {
    'first_name': fields.String(
        required=True, description='First name of the user'),
    'last_name': fields.String(
        required=True, description='Last name of the user'),
    'email': fields.String(
        required=True, description='Email of the user')
})


review_model = api.model('Review', {
    'review_text': fields.String(
        required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating (1-5)', min=1, max=5),
    'user_id': fields.Integer(
        required=True, description='ID of the user writing the review'),
    'place_id': fields.Integer(
        required=True, description='ID of the place being reviewed')
})


@api.route('/api/v1/users/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Create a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user['id'],
            'first_name': new_user['first_name'],
            'last_name': new_user['last_name'],
            'email': new_user['email']
        }, 201

    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        if not users:
            return {'error': 'No users found'}, 404
        return users, 200


@api.route('/api/v1/users/<int:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user, 200

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload
        user = facade.update_user(user_id, user_data)
        if not user:
            return {'error': 'User not found'}, 404
        return user, 200

    def delete(self, user_id):
        """Delete a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        facade.delete_user(user_id)
        return '', 204


@api.route('/api/v1/reviews/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review"""
        review_data = api.payload

        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 404

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        new_review = facade.create_review(review_data)
        return {
            'id': new_review['id'],
            'review_text': new_review['review_text'],
            'rating': new_review['rating'],
            'user_id': new_review['user_id'],
            'place_id': new_review['place_id']
        }, 201

    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        if not reviews:
            return {'error': 'No reviews found'}, 404
        return reviews, 200


@api.route('/api/v1/reviews/<int:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload
        review = facade.update_review(review_id, review_data)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    def delete(self, review_id):
        """Delete a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return '', 204


if __name__ == '__main__':
    facade = HBnBFacade()
    app.run(debug=True)
