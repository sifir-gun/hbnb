"""-Permet la création, modification, récupération et suppression des utilisateurs
-Endpoints pour gérer les utilisateurs via l'API (CRUD)
-Ajoute des routes pour GET et POST"""


from flask_restx import Namespace, Resource
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
"""Création du namespace pour l'API des utilisateurs"""
facade = HBnBFacade()
"""Utilisation de la Façade pour gérer les données"""


@api.route('/')
class UserList(Resource):
    def get(self):
        """Récupère tous les utilisateurs  .   Retourne la liste de tous les utilisateurs"""
        return facade.user_repo.get_all(), 200

    def post(self):
        """Crée un nouvel utilisateur"""
        new_user = {'id': 1, 'name': 'John Doe'}  # Exemple d'utilisateur
        # Ajoute l'utilisateur via le référentiel en mémoire
        facade.user_repo.add(new_user)
        return new_user, 201  # Retourne l'utilisateur créé avec le code HTTP 201
