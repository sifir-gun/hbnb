"""Endpoints API pour gérer les amenities (commodités).
Fournit des routes pour créer, modifier, récupérer et
supprimer des amenities via l'API.
"""

from flask import Flask, jsonify, request
from app.models.amenity import Amenity
from app.models import storage          # Pour accéder au stockage de données.

app = Flask(__name__)


# Route pour récupérer toutes les amenities (GET)


@app.route('/amenities', methods=['GET'])
def get_amenities():
    # On récupère toutes les instances de Amenity
    all_amenities = storage.all(Amenity).values()
    # On récupère toutes les instances de 'Amenity'
    amenities_list = [amenities.to_dict() for amenities in all_amenities]
    return jsonify(amenities_list), 200


# Route pour obtenir une amenity par ID (GET)


@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    # Permet d'identifier une commodité spécifique
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Amenity not found"}), 404
    return jsonify(amenity.to_dict()), 200


# Route pour créer une nouvelle amenity (POST)


@app.route('/amenities', methods=['POST'])
def create_amenity():
    # Vérifie si la requête contient du JSON et si le champ 'name' est présent
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Name is required"}), 400

    # Vérifie si la valeur de 'name' est bien une chaîne de caractères
    if not isinstance(request.json.get('name'), str):
        return jsonify({"error": " Name must be string"}), 400

    # Créer une nouvelle instance Amenity
    new_amenity = Amenity(name=request.json['name'])
    # On ajoute la nouvelle amenity au stockage
    storage.new(new_amenity)
    # Sauvegarde la nouvelle amenity
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


# Route pour mettre à jour une amenity (PUT)


@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    # Récupère l'instance d'Amenity
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Amenity not found"}), 404

    if not request.json:
        # Vérifie si le corps de la requête est bien en format JSON
        return jsonify({"error": "Resquest must be json"}), 400

    # Met à jour le nom de la commodité
    amenity.name = request.json.get('name', amenity.name)

    storage.save()
    return jsonify(amenity.to_dict()), 200
