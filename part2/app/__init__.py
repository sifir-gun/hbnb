from flask import Flask
from flask_restx import Api
from app.api.v1.places import api as places_api  # Use Namespace for places
from app.api.v1.users import api as users_api
from app.api.v1.reviews import api as reviews_api
from app.api.v1.amenities import api as amenities_api


def create_app():
    app = Flask(__name__)  # Créer et configurer l'application Flask
    # Initialisation de l'API Flask-RESTx
    api = Api(app, version='1.0', title='HBnB',
              description='HBnB Application API')

    # Register namespaces for all resources, including places
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(reviews_api, path='/api/v1/reviews')
    api.add_namespace(amenities_api, path='/api/v1/amenities')
    # Register places namespace
    api.add_namespace(places_api, path='/api/v1/places')

    return app
