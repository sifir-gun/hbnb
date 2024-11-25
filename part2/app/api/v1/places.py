"""
API Endpoints to manage places.
Provides routes to create, retrieve, update, and delete places via the API.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models import storage

# Declare the API Namespace for place-related operations
api = Namespace('places', description="Operations related to places")

# Data model for a place, used for API validation and documentation
place_model = api.model('Place', {
    'id': fields.String(required=False, description='ID of the place'),
    'title': fields.String(
        required=True,
        description='Title of the place',
        example="Macao"
    ),
    'description': fields.String(
        description='Description of the place',
        example="very good"
    ),
    'price': fields.Float(
        required=True,
        description='Price per night',
        example="120.23"
    ),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place',
        example="33.33"
    ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place',
        example="44.44"
    ),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(
        fields.String,
        required=True,
        description="List of amenities ID's",
        example=["BBQ"]
    )
})

# Instance of the facade to handle place-related data operations
facade = HBnBFacade()


def validate_place_data(data, is_update=False):
    """
    Validate data for creating or updating a place.

    Args:
        data (dict): Place data to validate.
        is_update (bool): Indicates if the validation is for an update.

    Returns:
        dict or None: Returns an error message if validation fails,
        otherwise None.
    """
    if 'price' in data and not isinstance(data['price'], (int, float)):
        return {"error": "Price must be a number"}, 400
    if 'amenities' in data and not isinstance(data['amenities'], list):
        return {"error": "Amenities must be a list"}, 400
    return None


@api.route('/')
class PlaceList(Resource):
    """
    Resource to manage the list of places.
    Provides operations to retrieve, create, and delete all places.
    """

    @api.doc('get_places')
    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'No places found')
    def get(self):
        """
        Retrieve all places from storage.

        Returns:
            list or dict: Returns a list of places or an error message.
        """
        try:
            places = storage.get_all(Place)
            if not places:
                return {"message": "No places found"}, 404

            # Convert each place to a dictionary for JSON output
            places_list = [place.to_dict()
                           for place in places if isinstance(place, Place)]
            return places_list, 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500

    @api.doc('create_place')
    # Validates incoming request data
    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)    # Formats API response data
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new place with the provided data.

        Returns:
            dict: Details of the created place or an error message.
        """
        place_data = api.payload
        # Validate place data
        validation_error = validate_place_data(place_data)
        if validation_error:
            return validation_error

        try:
            new_place = facade.create_place(place_data)
        except Exception as e:
            return {'error': f"Server error: {str(e)}"}, 500

        return new_place.to_dict(), 201

    @api.response(200, 'All places deleted successfully')
    def delete(self):
        """
        Delete all places from storage.

        Returns:
            dict: Message confirming the deletion of all places.
        """
        storage.clear_all(Place)
        storage.save()
        return {"message": "All places deleted successfully"}, 200


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceDetail(Resource):
    """
    Resource to manage operations on a specific place.
    Provides operations to retrieve, update, and delete a place by ID.
    """

    @api.doc('get_place')
    @api.expect(place_model, validate=True) # Valide automatiquement les données de la requête entrante
    @api.marshal_with(place_model)          # Structurer et formater la réponse de l’API
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details of a place by its ID.

        Args:
            place_id (str): ID of the place to retrieve.

        Returns:
            dict: Place details or error message if place is not found.
        """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """
        Update details of a place by its ID with the provided data.

        Args:
            place_id (str): ID of the place to update.

        Returns:
            dict: Updated place details or error message if place is not found.
        """
        data = request.json
        # Validate update data
        validation_error = validate_place_data(data, is_update=True)
        if validation_error:
            return validation_error

        # Update place via facade
        updated_place = facade.update_place(place_id, data)
        if isinstance(updated_place, tuple):  # Error handling
            return updated_place
        return updated_place.to_dict(), 200

    @api.doc('delete_place')
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """
        Delete a place by its ID.

        Args:
            place_id (str): ID of the place to delete.

        Returns:
            dict: Confirmation message or error message if place is not found.
        """
        # Delete place via facade
        result, status_code = facade.delete_place(place_id)
        return result, status_code

