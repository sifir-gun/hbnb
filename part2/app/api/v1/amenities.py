"""
API Endpoints to manage amenities.
Provides routes to create, update, retrieve, and delete amenities via the API.
"""

# app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create a namespace for grouping amenity-related routes
api = Namespace('amenities', description='Amenity operations')

# Define the Amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    # Required field "name" for each amenity
    'name': fields.String(required=True, description='Name of the amenity')
})

# Create an instance of HBnBFacade to handle business logic for amenities
facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    """Resource class for handling operations on the amenity collection"""

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload  # Retrieve data from request payload
        # Create a new amenity via the facade
        amenity, error = facade.create_amenity(amenity_data)
        # If an error occurs, return a 400 status with an error message
        if error:
            return {'error': error}, 400
        # Return the created amenity details with a 201 (created) status
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        # Retrieve the list of all amenities via the facade
        amenities = facade.get_all_amenities()
        # Return a list of amenities, each with its 'id' and 'name'
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Resource class for handling operations on a specific amenity by ID"""

    @api.response(200, 'Amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve an amenity by ID"""
        # Look up the amenity by ID via the facade
        amenity = facade.get_amenity(amenity_id)
        # If the amenity does not exist,
        # return a 404 status with an error message
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        # Return the amenity details with a 200 (OK) status
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity by ID"""
        amenity_data = api.payload  # Retrieve update data from request payload
        # Update the amenity via the facade
        amenity, error = facade.update_amenity(amenity_id, amenity_data)
        # If an error occurs, return a 400 status with an error message
        if error:
            return {'error': error}, 400
        # If the amenity does not exist,
        # return a 404 status with an error message
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        # Return a success message with a 200 (OK) status
        return {'message': 'Amenity updated successfully'}, 200

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity by ID"""
        # Delete the amenity by ID via the facade
        success = facade.delete_amenity(amenity_id)
        # If the amenity does not exist,
        # return a 404 status with an error message
        if not success:
            return {'error': 'Amenity not found'}, 404
        # Return a success message with a 200 (OK) status
        return {'message': 'Amenity deleted successfully'}, 200
