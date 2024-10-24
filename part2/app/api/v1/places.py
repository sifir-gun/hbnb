from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.place import Place
from app.models import storage


# Création de l'API Namespace pour les opérations liées aux places
api = Namespace('places', description="Operations related to places")

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True, description='Latitude of the place'),
    'longitude': fields.Float(
        required=True, description='Longitude of the place'),
    'owner': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(
        fields.String, required=True, description="List of amenities ID's"
    )
    })


def validate_place_data(data, is_update=False):
    """
    Valide les données reçues pour la création ou mise à jour d'un lieu.
    """
    required_fields = ['title', 'price', 'owner', 'amenities']

    if not is_update:
        # Pour la création, on vérifie que tous les champs obligatoires sont
        # présents
        for field in required_fields:
            if field not in data:
                return {"error": f"{field.capitalize()} is required"}, 400

    if 'price' in data and not isinstance(data['price'], (int, float)):
        return {"error": "Price must be a number"}, 400

    if 'amenities' in data and not isinstance(data['amenities'], list):
        return {"error": "Amenities must be a list"}, 400

    # On peut ajouter d'autres validations ici si nécessaire
    return None  # Pas d'erreur


@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def get(self):
        """ Récupérer tous les lieux depuis le stockage. """
        places = storage.get_all(Place)
        places_list = [place.to_dict() for place in places]
        return places_list, 200

    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Créer un nouveau lieu. """
        data = request.json
        validation_error = validate_place_data(data)
        if validation_error:
            return validation_error

        try:
            new_place = Place(
                id=None,  # L'ID est généré automatiquement
                title=data['title'],
                price=data['price'],
                owner=data['owner'],
                description=data.get('description', ""),  # Optionnel
                latitude=data.get('latitude'),  # Optionnel
                longitude=data.get('longitude')  # Optionnel
            )
            storage.add(new_place)
            storage.save()

            return new_place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

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
        place = storage.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """ Mettre à jour les informations d'un lieu. """
        place = storage.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        data = request.json
        validation_error = validate_place_data(data, is_update=True)
        if validation_error:
            return validation_error

        updatable_fields = [
            'title', 'price', 'owner', 'description', 'latitude', 'longitude'
        ]
        for field in updatable_fields:
            if field in data:
                setattr(place, field, data[field])

        storage.save()
        return place.to_dict(), 200

    def delete(self, place_id):
        """ Supprimer un lieu par son ID. """
        place = storage.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        storage.delete(place)
        storage.save()
        return {"message": "Place deleted successfully"}, 200
