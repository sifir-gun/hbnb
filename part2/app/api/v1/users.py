from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

"""
Ce module gère les endpoints CRUD (Create, Read, Update, Delete) pour les
utilisateurs via l'API. Il permet la création, la modification, la
récupération et la suppression des utilisateurs.

Les routes gérées incluent :
- POST pour créer un nouvel utilisateur
- GET pour récupérer les détails d'un utilisateur via son ID
- PUT pour mettre à jour un utilisateur via son ID
- DELETE pour supprimer un utilisateur via son ID
"""

# Création de l'espace de noms pour les opérations sur les utilisateurs
api = Namespace('users', description='User operations')

# Modèle utilisateur pour la validation des entrées et la documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True, description='First name of the user'),
    'last_name': fields.String(
        required=True, description='Last name of the user'),
    'email': fields.String(
        required=True, description='Email of the user')
})

# Instanciation de la façade pour les opérations utilisateur
facade = HBnBFacade()


@api.route('/')
class UserList(Resource):
    """
    Classe gérant les opérations sur la collection d'utilisateurs
    (liste d'utilisateurs).
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Crée un nouvel utilisateur.

        Cette méthode vérifie d'abord si l'email fourni est déjà enregistré.
        Si c'est le cas, elle retourne une erreur 400. Si l'email est unique,
        l'utilisateur est créé et ses détails sont renvoyés.

        Retourne :
            - 201 : Si l'utilisateur a été créé avec succès
            - 400 : Si l'email est déjà enregistré ou
            si les données sont invalides
        """
        user_data = api.payload

        # Vérification de l'unicité de l'email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Création d'un nouvel utilisateur via le service facade
        try:
            new_user = facade.create_user(user_data)
        except Exception as error:
            # Gestion des erreurs lors de la création de l'utilisateur
            return {'error': str(error)}, 400

        # Retourne les détails de l'utilisateur créé
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


@api.route('/<string:user_id>')
class UserResource(Resource):
    """
    Classe gérant les opérations sur un utilisateur spécifique (via son ID).
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Récupère les détails d'un utilisateur en fonction de son ID.

        Retourne :
            - 200 : Si l'utilisateur a été trouvé et ses détails sont renvoyés
            - 404 : Si l'utilisateur n'existe pas
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Retourne les détails de l'utilisateur trouvé
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur en fonction de son ID.

        Cette méthode vérifie d'abord si l'utilisateur existe.
        Si c'est le cas, elle met à jour les informations de l'utilisateur.

        Retourne :
            - 200 : Si l'utilisateur a été mis à jour avec succès
            - 404 : Si l'utilisateur n'existe pas
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Récupération des nouvelles données de l'utilisateur
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
        except Exception as error:
            return {'error': str(error)}, 400

        # Retourne les détails de l'utilisateur mis à jour
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """
        Supprime un utilisateur en fonction de son ID.

        Retourne :
            - 200 : Si l'utilisateur a été supprimé avec succès
            - 404 : Si l'utilisateur n'existe pas
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Suppression de l'utilisateur
        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
