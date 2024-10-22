import uuid
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
# -Permet la création, modification, récupération et
# suppression des utilisateurs
# -Endpoints pour gérer les utilisateurs via l'API (CRUD)
# -Ajoute des routes pour GET et POST
api = Namespace('users', description='User operations')
"""Création du namespace pour l'API des utilisateurs"""
# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(required=True, description='Email of the user')
})
facade = HBnBFacade()
"""Utilisation de la Façade pour gérer les données"""


@api.route('/')
class UserList(Resource):
    def get(self):
        """Récupère tous les utilisateurs  .
        Retourne la liste de tous les utilisateurs"""
        return facade.user_repo.get_all(), 200

    @api.expect(user_model)
    def post(self):
        """Crée un nouvel utilisateur"""
        data = api.payload  # Récupère les données envoyées dans la requête
        if not data:
            return {"error": "No input data provided"}, 400
        # Génère un ID unique pour le nouvel utilisateur
        data['id'] = str(uuid.uuid4())  # Génère un UUID
        # Ajoute l'utilisateur via le référentiel en mémoire
        try:
            new_user = facade.user_repo.add(data)
        except Exception as e:
            return {"error": str(e)}, 500
        # Retourne l'utilisateur créé avec le code HTTP 201
        return new_user, 201
