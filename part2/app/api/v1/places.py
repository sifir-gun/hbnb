from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models import storage


api = Namespace('places', description="Operations related to places")

place_model = api.model('Place', {
    'id': fields.String(required=False, description='Title of the place'),
    'title': fields.String(required=True, description='Title of the place', example="Macao"),
    'description': fields.String(description='Description of the place', example="very good"),
    'price': fields.Float(required=True, description='Price per night', example="120.23"),
    'latitude': fields.Float(required=True, description='Latitude of the place', example="33.33"),
    'longitude': fields.Float(required=True, description='Longitude of the place', example="44.44"),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's", example=["BBQ"])
})

facade = HBnBFacade()


def validate_place_data(data, is_update=False):
    if 'price' in data and not isinstance(data['price'], (int, float)):
        return {"error": "Price must be a number"}, 400
    if 'amenities' in data and not isinstance(data['amenities'], list):
        return {"error": "Amenities must be a list"}, 400
    return None


@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def get(self):
        """ Récupérer tous les lieux depuis le stockage. """
        try:
            places = storage.get_all(Place)
            if not places:
                return {"message": "Aucun lieu trouvé"}, 404

            places_list = [place.to_dict()
                           for place in places if isinstance(place, Place)]
            return places_list, 200
        except Exception as e:
            return {"error": f"Erreur serveur : {str(e)}"}, 500

    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Créer un nouveau lieu. """
        place_data = api.payload
        validation_error = validate_place_data(place_data)
        if validation_error:
            return validation_error

        try:
            new_place = facade.create_place(place_data)
        
        except Exception as e:
            return {'error': f"Erreur serveur : {str(e)}"}, 500

        return new_place.to_dict(), 201

    @api.response(200, 'All places deleted successfully')
    def delete(self):
        """ Supprimer tous les lieux. """
        storage.clear_all(Place)
        storage.save()
        return {"message": "All places deleted successfully"}, 200


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceDetail(Resource):
    @api.doc('get_place')
    @api.expect(place_model, validate=True)
    @api.marshal_with(place_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """ Récupérer les détails d'un lieu par son ID. """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """ Mettre à jour les informations d'un lieu. """
        data = request.json
        validation_error = validate_place_data(data, is_update=True)
        if validation_error:
            return validation_error

        # Mise à jour du lieu via la façade
        updated_place = facade.update_place(place_id, data)
        if isinstance(updated_place, tuple):  # Gestion des erreurs
            return updated_place
        return updated_place.to_dict(), 200

    
    def delete(self, place_id):
        """ Supprimer un lieu par son ID. """
        print(f"Deleting place with ID: {place_id}")

        # Suppression du lieu via la façade
        result, status_code = facade.delete_place(place_id)
        return result, status_code
