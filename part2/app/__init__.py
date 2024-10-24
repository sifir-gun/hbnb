from flask import Flask
from flask_restx import Api
# Importation du namespace API des places
from app.api.v1.places import api as places_api
# Importation du namespace API des utilisateurs
from app.api.v1.users import api as users_api
"""
Initialise Flask et configure l'API Flask-RESTx
pip install flask-restx. Facilite la création d'API RESTful en Python
"""


def create_app():
    app = Flask(__name__)
    """Créer et configurer l'application Flask."""

    api = Api(app, version='1.0', title='HBnB',
              description='HBnB Application API')

    # Ajout des namespaces pour les places et les utilisateurs
    # Namespace pour les places
    api.add_namespace(places_api, path='/api/v1/places')
    # Namespace pour les utilisateurs
    api.add_namespace(users_api, path='/api/v1/users')

    return app
