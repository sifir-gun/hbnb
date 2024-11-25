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

# Creating the namespace for user-related operations
api = Namespace('users', description='User operations')

# User model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True, description='First name of the user'),
    'last_name': fields.String(
        required=True, description='Last name of the user'),
    'email': fields.String(
        required=True, description='Email of the user')
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

        # Check for unique email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create a new user via the facade service
        try:
            new_user = facade.create_user(user_data)
        except Exception as error:
            # Handle errors during user creation
            return {'error': str(error)}, 400

        # Return the details of the created user
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


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

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details by ID.

        This method first checks if the user exists.
        If so, it updates the user’s information.

        Returns:
            - 200: If the user was successfully updated
            - 404: If the user does not exist
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Retrieve updated user data
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
        except Exception as error:
            return {'error': str(error)}, 400

        # Return the details of the updated user
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

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

        # Delete the user
        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
