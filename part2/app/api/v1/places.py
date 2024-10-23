from flask_restx import Namespace, Resource
from flask import request
from app.models.place import Place
from app.models import storage

"""Endpoints API for managing places."""

# Create a Namespace for places
api = Namespace('places', description="Place operations")


# Route to get all places (GET)
@api.route('/')
class PlaceList(Resource):
    def get(self):
        all_places = storage.all(Place).values()
        places_list = [place.to_dict() for place in all_places]
        return places_list, 200  # No need to jsonify, Flask-RESTx handles it

    def post(self):
        """Create a new place"""
        data = request.json
        if not data or 'name' not in data:
            return {"error": "Name is required"}, 400
        new_place = Place(
            name=data['name'],
            description=data.get('description', "")
        )
        storage.new(new_place)
        storage.save()
        return new_place.to_dict(), 201


# Route to get a specific place by ID (GET)
@api.route('/<place_id>')
class PlaceDetail(Resource):
    def get(self, place_id):
        place = storage.get(Place, place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    def put(self, place_id):
        """Update an existing place"""
        place = storage.get(Place, place_id)
        if not place:
            return {"error": "Place not found"}, 404
        if not request.json:
            return {"error": "Request body must be JSON"}, 400
        place.name = request.json.get('name', place.name)
        place.description = request.json.get('description', place.description)
        storage.save()
        return place.to_dict(), 200
