"""
API Endpoints for administrator operations.
Provides routes for admin-only actions like user management and
amenity control.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('admin', description='Admin operations')
facade = HBnBFacade()

# API Models
user_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(default=False, description='Admin status')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


def admin_required():
    """Vérifie si l'utilisateur est un administrateur"""
    current_user = get_jwt_identity()
    if not current_user.get('is_admin'):
        return {'error': 'Admin privileges required'}, 403
    return None


@api.route('/users')
class AdminUserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        auth_error = admin_required()
        if auth_error:
            return auth_error

        try:
            new_user = facade.create_user(api.payload)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update any user's details (admin only)"""
        auth_error = admin_required()
        if auth_error:
            return auth_error

        try:
            updated_user = facade.admin_update_user(user_id, api.payload)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/amenities')
class AdminAmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        auth_error = admin_required()
        if auth_error:
            return auth_error

        try:
            new_amenity = facade.create_amenity(api.payload)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/amenities/<amenity_id>')
class AdminAmenityResource(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update any amenity (admin only)"""
        auth_error = admin_required()
        if auth_error:
            return auth_error

        try:
            updated_amenity = facade.admin_update_amenity(
                amenity_id, api.payload)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
