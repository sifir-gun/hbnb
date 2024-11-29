"""
API Endpoints to manage places.
Provides routes to create, retrieve, update, and delete places via the API.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models import storage

# Declare the API Namespace for place-related operations
api = Namespace('places', description="Operations related to places")

# Data model for a place
place_model = api.model('Place', {
    'owner_id': fields.String(required=False, description='ID of the place'),
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
    'amenities': fields.List(
        fields.String,
        required=True,
        description="List of amenities ID's",
        example=["BBQ"]
    )
})

facade = HBnBFacade()


def validate_place_data(data, is_update=False):
    """Validate place data"""
    if 'price' in data and not isinstance(data['price'], (int, float)):
        return {"error": "Price must be a number"}, 400
    if 'amenities' in data and not isinstance(data['amenities'], list):
        return {"error": "Amenities must be a list"}, 400
    return None


@api.route('/')
class PlaceList(Resource):
    @api.doc('get_places')
    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'No places found')
    def get(self):
        """Public endpoint: Retrieve all places from storage."""
        try:
            places = storage.get_all(Place)
            if not places:
                return {"message": "No places found"}, 404

            places_list = [place.to_dict()
                           for place in places if isinstance(place, Place)]
            return places_list, 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500

    @api.doc('create_place')
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Protected endpoint: Create a new place"""
        current_user = get_jwt_identity()
        print(f"User authenticated: {current_user}")  # Log utilisateur

        place_data = api.payload
        print(f"Received payload: {place_data}")  # Log des données reçues

        place_data['owner_id'] = current_user['id']
        validation_error = validate_place_data(place_data)
        if validation_error:
            # Log d'erreur de validation
            print(f"Validation error: {validation_error}")
            return validation_error

        try:
            new_place = facade.create_place(place_data)
            print(f"Created place: {new_place}")  # Log de l'objet Place créé
            return new_place.to_dict(), 201
        except Exception as e:
            print(f"Error creating place: {str(e)}")  # Log des erreurs
            return {'error': str(e)}, 400


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceDetail(Resource):
    @api.doc('get_place')
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Public endpoint: Get place details"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Protected endpoint: Update place details"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        # Verify ownership
        if place.owner_id != current_user['id']:
            return {"error": "Unauthorized action"}, 403

        validation_error = validate_place_data(api.payload, is_update=True)
        if validation_error:
            return validation_error

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.doc('delete_place')
    @api.response(200, 'Place deleted successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Protected endpoint: Delete place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        # Verify ownership
        if place.owner_id != current_user['id']:
            return {"error": "Unauthorized action"}, 403

        try:
            facade.delete_place(place_id)
            return {"message": "Place deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/user/places')
class UserPlaces(Resource):
    @api.doc('get_user_places')
    @api.response(200, 'List of user places retrieved successfully')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def get(self):
        """Protected endpoint: Retrieve all places for the authenticated user."""
        current_user = get_jwt_identity()  # Récupérer l'utilisateur courant
        user_id = current_user['id']

        try:
            # Récupérer les lieux appartenant à cet utilisateur
            user_places = storage.query(
                Place).filter_by(owner_id=user_id).all()
            if not user_places:
                return {"message": "No places found for this user"}, 404

            # Retourner la liste des lieux sous forme de dictionnaire
            return [place.to_dict() for place in user_places], 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500
