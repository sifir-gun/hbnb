from flask import request
from flask_restx import Namespace, Resource
from app.models.place import Place
from app.models import storage

# Création de l'API Namespace
api = Namespace('places', description="Operations related to places")


@api.route('/')
class PlaceList(Resource):
    def get(self):
        """
        Récupérer tous les lieux depuis le stockage.
        """
        places = storage.get_all(Place)
        places_list = [place.to_dict() for place in places]
        return places_list, 200

    def post(self):
        """
        Créer un nouveau lieu.
        """
        if not request.json or 'title' not in request.json:
            return {"error": "Title is required"}, 400
        if 'price' not in request.json:
            return {"error": "Price is required"}, 400
        if 'owner' not in request.json:
            return {"error": "Owner is required"}, 400

        try:
            new_place = Place(
                title=request.json['title'],
                price=request.json['price'],
                owner=request.json['owner'],
                description=request.json.get('description', ""),
                latitude=request.json.get('latitude', None),
                longitude=request.json.get('longitude', None)
            )
            storage.add(new_place)
            storage.save()

            return new_place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def delete(self):
        """
        Supprimer tous les lieux.
        """
        storage.clear_all(Place)
        storage.save()
        return {"message": "All places deleted successfully"}, 200


@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    def get(self, place_id):
        """
        Récupérer les détails d'un lieu par ID.
        """
        place = storage.get(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    def put(self, place_id):
        """
        Mettre à jour un lieu spécifique par ID.
        """
        place = storage.get(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        if not request.json:
            return {"error": "Request body must be JSON"}, 400

        updatable_fields = ['title', 'price', 'owner',
                            'description', 'latitude', 'longitude']
        for field in updatable_fields:
            if field in request.json:
                setattr(place, field, request.json[field])

        storage.save()
        return place.to_dict(), 200

    def delete(self, place_id):
        """
        Supprimer un lieu par ID.
        """
        place = storage.get(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        storage.delete(place)
        storage.save()
        return {"message": "Place deleted successfully"}, 200
