"""Endpoints API pour gérer les places (logements).
Fournit des routes pour créer, modifier, récupérer et supprimer des places via l'API."""


from flask import Flask, jsonify, request
from models.place import Place
from models import storage              # Pour accéder au stockage de données.
app = Flask(__name__)


"""Route pour obtenir des places"""


@app.route('/places', methods=['GET'])
def get_places():

    # Récupère toutes les instances de Place
    all_places = storage.all(Place).values()
    places_list = [place.to_dict()
                   for place in all_places]     # Convertir en JSON
    return jsonify(places_list), 200


"""Route pour obtenir une place spécifique par son ID"""


@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    # Récupère la place de son ID
    place = storage.get(Place, place_id)
    if place is None:
        # Gestion des erreurs
        return jsonify({"error": "Place not found"}), 404
    return jsonify(place.to_dict()), 200


"""Route pour créer une nouvelle place"""


@app.route('/places', methods=['POST'])
def create_place():
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Name is required"}), 400

    """Créer une nouvelle instance de place"""
    new_place = Place(name=request.json['name'],
                      description=request.json.get('description', ""))
    """ajoute une nouvelle place au storage"""
    storage.new(new_place)
    """Sauvegarde la nouvelle place"""
    storage.save()
    return jsonify(new_place.to_dict()), 201


"""Route pour mettre à jour une place"""


@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": " Place not found"}), 404

    if not request.json:
        return jsonify({"error": "Request body must be JSON"}), 400

    """Mise à jour des champs modifiés"""
    place.name = request.json.get('name', place.name)
    place.description = request.json.get('description', place.description)

    storage.save()
    return jsonify(place.to_dict()), 200


"""Route pour supprimer une place"""


@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Place not found"}), 404

    storage.delete(place)                       # Supprime la place
    storage.save()                              # Sauvegarde les changements
    return jsonify({"message": "Place deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
