"""initialise la version 1 de l'API."""
"""Cette couche API reçoit les requêtes HTTP des utilisateurs"""


from flask_restx import Api
from flask import Blueprint
from .users import api as users_api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
"""Création du blueprint pour l'API"""

api = Api(api_bp, version='1.0', title='HBnB API',
          description='API pour gérer les entités HBnB')

"""Enregistrement du namespace dans l'API"""
api.add_namespace(users_api)
