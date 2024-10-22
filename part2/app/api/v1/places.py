from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource
from app.models.place import Place
from app.models import storage

"""Endpoints API pour gérer les places (logements).
Fournit des routes pour créer, modifier,
récupérer et supprimer des places via l'API."""

# Pour accéder au stockage de données
# Création du Blueprint et de l'API Namespace
places_app = Blueprint('places_app', __name__)
api = Namespace('places', description="Places operations")
# Route pour récupérer toutes les places (GET)


@api.route('/')
class PlaceList(Resource):
    def get(self):
        all_places = storage.all(Place).values()
        places_list = [place.to_dict() for place in all_places]
        return jsonify(places_list), 200
# Route pour récupérer une place spécifique par ID (GET)


@api.route('/<place_id>')
class PlaceDetail(Resource):
    def get(self, place_id):
        place = storage.get(Place, place_id)
        if place is None:
            return jsonify({"error": "Place not found"}), 404
        return jsonify(place.to_dict()), 200
# Route pour créer une nouvelle place (POST)


@api.route('/')
class PlaceCreate(Resource):
    def post(self):
        data = request.json
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
        new_place = Place(
            name=data['name'],
            description=data.get('description', "")
            )
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
# Route pour mettre à jour une place existante (PUT)


@api.route('/<place_id>')
class PlaceUpdate(Resource):
    def put(self, place_id):
        place = storage.get(Place, place_id)
        if place is None:
            return jsonify({"error": "Place not found"}), 404
        if not request.json:
            return jsonify({"error": "Request body must be JSON"}), 400
        place.name = request.json.get('name', place.name)
        place.description = request.json.get('description', place.description)
        storage.save()
        return jsonify(place.to_dict()), 200
