"""Endpoints API pour gérer les amenities (commodités).
Fournit des routes pour créer, modifier, récupérer et
supprimer des amenities via l'API.
"""

# app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Création d'un namespace pour regrouper les routes liées aux commodités (amenities)
api = Namespace('amenities', description='Amenity operations')

# Définition du modèle Amenity pour la validation et la documentation des données d'entrée
amenity_model = api.model('Amenity', {
    # Champ "name" requis pour chaque commodité
    'name': fields.String(required=True, description='Name of the amenity')
})

# Création de l'instance de HBnBFacade pour gérer la logique métier liée aux commodités
facade = HBnBFacade()

# Définition de la classe pour les routes sur la collection des commodités (AmenityList)


@api.route('/')
class AmenityList(Resource):
    # Spécifie que les données d'entrée doivent respecter le modèle amenity_model
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Créer une nouvelle commodité"""
        amenity_data = api.payload  # Récupère les données envoyées dans le corps de la requête
        # Crée une nouvelle commodité via la façade
        amenity, error = facade.create_amenity(amenity_data)
        if error:  # Si une erreur survient, retourne un code 400 avec un message d'erreur
            return {'error': error}, 400
        return {  # Retourne les informations de la commodité créée avec un code 201 (créé avec succès)
            'id': amenity.id,
            'name': amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Récupérer toutes les commodités"""
        amenities = facade.get_all_amenities(
        )  # Récupère la liste de toutes les commodités via la façade
        # Retourne la liste des commodités, chaque commodité ayant son 'id' et 'name'
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


# Définition de la classe pour les routes sur une commodité spécifique par ID (AmenityResource)
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Récupérer une commodité par ID"""
        amenity = facade.get_amenity(
            amenity_id)  # Recherche la commodité par son ID via la façade
        if not amenity:  # Si la commodité n'existe pas, retourne un code 404 avec un message d'erreur
            return {'error': 'Amenity not found'}, 404
        # Retourne les informations de la commodité trouvée avec un code 200 (OK)
        return {'id': amenity.id, 'name': amenity.name}, 200

    # Spécifie que les données d'entrée doivent respecter le modèle amenity_model
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Mettre à jour une commodité par ID"""
        amenity_data = api.payload  # Récupère les données de mise à jour envoyées dans le corps de la requête
        # Met à jour la commodité via la façade
        amenity, error = facade.update_amenity(amenity_id, amenity_data)
        if error:  # Si une erreur survient, retourne un code 400 avec un message d'erreur
            return {'error': error}, 400
        if not amenity:  # Si la commodité n'existe pas, retourne un code 404 avec un message d'erreur
            return {'error': 'Amenity not found'}, 404
        # Retourne un message de succès avec un code 200 (OK)
        return {'message': 'Amenity updated sucessfully'}, 200

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Supprimer une commodité par ID"""
        success = facade.delete_amenity(
            amenity_id)  # Supprime la commodité par son ID via la façade
        if not success:  # Si la commodité n'existe pas, retourne un code 404 avec un message d'erreur
            return {'error': 'Amenity not found'}, 404
        # Retourne un message de succès avec un code 200 (OK)
        return {'message': 'Amenity deleted successfully'}, 200
