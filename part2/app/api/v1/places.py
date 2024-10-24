from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models import storage


# Création de l'API Namespace pour les opérations liées aux places
api = Namespace('places', description="Operations related to places")

place_model = api.model('Place', {
    'id': fields.String(required=False, description='Title of the place'),
    'title': fields.String(required=True, description='Title of the place', example="Macao"),
    'description': fields.String(description='Description of the place', example="very good"),
    'price': fields.Float(required=True, description='Price per night', example="120.23"),
    'latitude': fields.Float(
        required=True, description='Latitude of the place', example="33.33"),
    'longitude': fields.Float(
        required=True, description='Longitude of the place', example="44.44"),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(
        fields.String, required=True, description="List of amenities ID's", example=["BBQ"])
})

facade = HBnBFacade()


def validate_place_data(data, is_update=False):
    """
    Valide les données reçues pour la création ou mise à jour d'un lieu.
    """
    required_fields = ['title', 'price', 'owner_id', 'amenities']

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

    return None  # Pas d'erreur


@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def get(self):
        """ Récupérer tous les lieux depuis le stockage. """
        try:
            # Récupération de tous les lieux depuis le stockage
            places = storage.get_all(Place)
            # Vérification s'il y a des lieux
            if not places:
                return {"message": "Aucun lieu trouvé"}, 404

            # Sérialisation des lieux sous forme de dictionnaire
            places_list = [place.to_dict() for place in places]
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

        # Appeler la fonction de validation pour vérifier les champs
        validation_error = validate_place_data(place_data)
        if validation_error:
            return validation_error

        try:
            # Création du lieu via la façade
            new_place = facade.create_place(place_data)
        except ValidationError as error:
            # Gestion des erreurs de validation
            return {'error': str(error)}, 400
        except Exception as e:
            # Gestion des erreurs générales
            return {'error': f"Erreur serveur : {str(e)}"}, 500

        # Retourne les détails du lieu créé
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id,
            'amenities': [],
        }, 201

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
            'title', 'price', 'owner_id', 'description', 'latitude', 'longitude'
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
