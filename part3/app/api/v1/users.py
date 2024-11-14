"""
This module manages CRUD (Create, Read, Update, Delete) endpoints
for users via the API.
It allows for creating, updating, retrieving, and deleting users.

The managed routes include:
- POST to create a new user
- GET to retrieve user details by ID
- PUT to update a user by ID
- DELETE to delete a user by ID
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Creating the namespace for user-related operations
api = Namespace('users', description='User operations')

# User model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True, description='First name of the user'),
    'last_name': fields.String(
        required=True, description='Last name of the user'),
    'email': fields.String(
        required=True, description='Email of the user'),
    'password': fields.String(
        required=True, description='Password')
})

# Instantiating the facade for user operations
facade = HBnBFacade()


@api.route('/')
class UserList(Resource):
    """
    Class to handle operations on the user collection (list of users).
    Provides methods to create and retrieve users.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new user.

        This method first checks if the provided email is already registered.
        If so, it returns a 400 error. If the email is unique,
        the user is created, and the details are returned.

        Returns:
            - 201: If the user was successfully created
            - 400: If the email is already registered or
                   if the data is invalid
        """
        user_data = api.payload
        print("\n=== Creating User via API ===")
        print(f"Received request to create user with email: {user_data.get(
            'email')}")

        # Check for unique email first
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            print(f"Email {user_data['email']} already exists")
            return {'error': 'Email already registered'}, 400

        try:
            # Pass the raw data to facade - no password hashing here
            new_user = facade.create_user(user_data)
            print("User created successfully")

            # Return user details (excluding password)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

        except ValueError as error:
            print(f"Error creating user: {str(error)}")
            return {'error': str(error)}, 400


@api.route('/<string:user_id>')
class UserResource(Resource):
    """
    Class to handle operations on a specific user (by ID).
    Provides methods to retrieve, update, and delete a user by ID.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve user details by ID.

        Returns:
            - 200: If the user is found and the details are returned
            - 404: If the user does not exist
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Return the details of the found user
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details by ID.

        Returns:
            - 200: If the user was successfully updated
            - 404: If the user does not exist
        """
        """Protected endpoint: Update user details"""
        current_user = get_jwt_identity()

        # Verify user is modifying their own data
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Check for restricted fields
        if 'email' in api.payload or 'password' in api.payload:
            return {
                'error': 'You cannot modify email or password through this '
                         'endpoint'
            }, 400

        try:
            updated_user = facade.update_user(user_id, api.payload)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """
        Delete a user by ID.

        Returns:
            - 200: If the user was successfully deleted
            - 404: If the user does not exist
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'You have accessed a protected resource.'}
