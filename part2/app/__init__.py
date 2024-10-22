"""Initialise Flask et configure l'API Flask-RESTx"""
from flask import Flask
from flask_restx import Api
from app.api.v1.places import places_app
from app.api.v1.users import api as users_api


def create_app():
    app = Flask(__name__)  # Créer et configurer l'application Flask
    # Initialisation de l'API Flask-RESTx
    api = Api(app, version='1.0', title='HBnB',
              description='HBnB Application API')
    # Enregistre le Blueprint des routes de places.py avec un préfixe
    app.register_blueprint(places_app, url_prefix='/api/v1')
    # Ajout du namespace pour les utilisateurs
    api.add_namespace(users_api, path='/api/v1/users')
    return app
