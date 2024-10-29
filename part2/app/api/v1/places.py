from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models import storage

# Déclaration de l'API Namespace pour les opérations liées aux lieux
api = Namespace('places', description="Operations related to places")

# Modèle de données pour un lieu, utilisé pour la validation et la documentation de l'API
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

# Instance de la façade pour gérer les opérations de données liées aux lieux
facade = HBnBFacade()

def validate_place_data(data, is_update=False):
    """
    Valide les données de création ou de mise à jour d'un lieu.
    
    Args:
        data (dict): Les données du lieu à valider.
        is_update (bool): Indique si la validation est pour une mise à jour.

    Returns:
        dict ou None: Retourne un message d'erreur si une validation échoue, sinon None.
    """
    if 'price' in data and not isinstance(data['price'], (int, float)):
        return {"error": "Price must be a number"}, 400
    if 'amenities' in data and not isinstance(data['amenities'], list):
        return {"error": "Amenities must be a list"}, 400
    return None


@api.route('/')
class PlaceList(Resource):
    """
    Ressource pour gérer la liste des lieux.
    Fournit les opérations pour récupérer, créer, et supprimer tous les lieux.
    """
    
    @api.doc('create_place')
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def get(self):
        """
        Récupère tous les lieux depuis le stockage.
        
        Returns:
            list ou dict: Retourne une liste de lieux ou un message d'erreur.
        """
        try:
            places = storage.get_all(Place)
            if not places:
                return {"message": "Aucun lieu trouvé"}, 404

            # Conversion de chaque lieu en dictionnaire pour l'affichage JSON
            places_list = [place.to_dict() for place in places if isinstance(place, Place)]
            return places_list, 200
        except Exception as e:
            return {"error": f"Erreur serveur : {str(e)}"}, 500

    @api.doc('create_place')
    @api.expect(place_model)                    # Valide automatiquement les données de la requête entrante
    @api.marshal_with(place_model, code=201)    # Structurer et formater la réponse de l’API
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Crée un nouveau lieu avec les données fournies.
        
        Returns:
            dict: Retourne les détails du lieu créé ou un message d'erreur.
        """
        place_data = api.payload
        # Validation des données de lieu
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
        """
        Supprime tous les lieux du stockage.
        
        Returns:
            dict: Message confirmant la suppression de tous les lieux.
        """
        storage.clear_all(Place)
        storage.save()
        return {"message": "All places deleted successfully"}, 200


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceDetail(Resource):
    """
    Ressource pour gérer les opérations sur un lieu spécifique.
    Fournit les opérations pour récupérer, mettre à jour et supprimer un lieu par ID.
    """

    @api.doc('get_place')
    # @api.expect(place_model, validate=True) # Valide automatiquement les données de la requête entrante
    @api.marshal_with(place_model)          # Structurer et formater la réponse de l’API
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Récupère les détails d'un lieu par son ID.
        
        Args:
            place_id (str): ID du lieu à récupérer.
        
        Returns:
            dict: Détails du lieu ou message d'erreur si le lieu n'est pas trouvé.
        """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """
        Met à jour les informations d'un lieu par son ID avec les données fournies.
        
        Args:
            place_id (str): ID du lieu à mettre à jour.
        
        Returns:
            dict: Détails du lieu mis à jour ou message d'erreur si le lieu n'est pas trouvé.
        """
        data = request.json
        # Validation des données de mise à jour
        validation_error = validate_place_data(data, is_update=True)
        if validation_error:
            return validation_error

        # Mise à jour du lieu via la façade
        updated_place = facade.update_place(place_id, data)
        if isinstance(updated_place, tuple):  # Gestion des erreurs
            return updated_place
        return updated_place.to_dict(), 200

    def delete(self, place_id):
        """
        Supprime un lieu par son ID.
        
        Args:
            place_id (str): ID du lieu à supprimer.
        
        Returns:
            dict: Message de confirmation ou message d'erreur si le lieu n'est pas trouvé.
        """
        print(f"Deleting place with ID: {place_id}")

        # Suppression du lieu via la façade
        result, status_code = facade.delete_place(place_id)
        return result, status_code

