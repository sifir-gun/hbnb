from flask import request
from flask_restx import Namespace, Resource
from app.models.place import Place
from app.models import storage

# Création de l'API Namespace pour les opérations liées aux places
api = Namespace('places', description="Operations related to places")


@api.route('/')
class PlaceList(Resource):
    """
    Ressource pour gérer la collection de lieux (places).
    Cette ressource permet de récupérer tous les lieux et d'en créer de nouveaux.
    """

    def get(self):
        """
        Récupérer tous les lieux depuis le stockage.

        Retourne une liste de tous les lieux avec un statut HTTP 200.
        """
        # Récupérer tous les objets 'Place' depuis le stockage
        places = storage.get_all(Place)

        # Convertir chaque objet 'Place' en dictionnaire pour la réponse JSON
        places_list = [place.to_dict() for place in places]

        # Retourner la liste des lieux et le code HTTP 200
        return places_list, 200

    def post(self):
        """
        Créer un nouveau lieu.

        Reçoit des données JSON avec les champs 'title', 'price', et 'owner'.
        Retourne le lieu créé avec le statut HTTP 201 ou une erreur 400 si une donnée est manquante.
        """
        # Vérifier si le corps de la requête est bien en JSON et contient les champs obligatoires
        if not request.json or 'title' not in request.json:
            return {"error": "Title is required"}, 400
        if 'price' not in request.json:
            return {"error": "Price is required"}, 400
        if 'owner' not in request.json:
            return {"error": "Owner is required"}, 400

        try:
            # Créer un nouveau lieu avec les données fournies
            new_place = Place(
                title=request.json['title'],
                price=request.json['price'],
                owner=request.json['owner'],
                description=request.json.get('description', ""),  # Optionnel
                latitude=request.json.get('latitude', None),  # Optionnel
                longitude=request.json.get('longitude', None)  # Optionnel
            )
            # Ajouter le lieu au stockage
            storage.add(new_place)
            storage.save()

            # Retourner les détails du lieu créé avec le code HTTP 201
            return new_place.to_dict(), 201
        except ValueError as e:
            # Gérer les erreurs de validation
            return {"error": str(e)}, 400

    def delete(self):
        """
        Supprimer tous les lieux.

        Retourne un message de confirmation avec le statut HTTP 200 après avoir supprimé tous les lieux.
        """
        # Supprimer tous les objets 'Place' du stockage
        storage.clear_all(Place)
        storage.save()

        # Retourner un message de confirmation et le code HTTP 200
        return {"message": "All places deleted successfully"}, 200


@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    """
    Ressource pour gérer un lieu spécifique par son ID.
    Cette ressource permet de récupérer, mettre à jour ou supprimer un lieu spécifique.
    """

    def get(self, place_id):
        """
        Récupérer les détails d'un lieu par son ID.

        Retourne les détails du lieu avec le statut HTTP 200 ou une erreur 404 si le lieu n'est pas trouvé.
        """
        # Récupérer le lieu spécifique à partir de son ID
        place = storage.get(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        # Retourner les détails du lieu et le code HTTP 200
        return place.to_dict(), 200

    def put(self, place_id):
        """
        Mettre à jour les informations d'un lieu spécifique par son ID.

        Reçoit des données JSON avec les champs à mettre à jour.
        Retourne les détails du lieu mis à jour avec le statut HTTP 200 ou une erreur 404 si le lieu n'est pas trouvé.
        """
        # Récupérer le lieu spécifique à partir de son ID
        place = storage.get(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        # Vérifier que le corps de la requête est bien en JSON
        if not request.json:
            return {"error": "Request body must be JSON"}, 400

        # Liste des champs qui peuvent être mis à jour
        updatable_fields = ['title', 'price', 'owner',
                            'description', 'latitude', 'longitude']

        # Mettre à jour les champs du lieu avec les nouvelles valeurs fournies
        for field in updatable_fields:
            if field in request.json:
                setattr(place, field, request.json[field])

        # Sauvegarder les modifications dans le stockage
        storage.save()

        # Retourner les détails du lieu mis à jour avec le code HTTP 200
        return place.to_dict(), 200

    def delete(self, place_id):
        """
        Supprimer un lieu par son ID.

        Retourne un message de confirmation avec un statut HTTP 200 ou une erreur 404 si le lieu n'est pas trouvé.
        """
        # Récupérer le lieu spécifique à partir de son ID
        place = storage.get(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        # Supprimer le lieu du stockage
        storage.delete(place)
        storage.save()

        # Retourner un message de confirmation avec le code HTTP 200
        return {"message": "Place deleted successfully"}, 200
