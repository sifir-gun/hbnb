<<<<<<< HEAD
from flask import Flask
from flask_restx import Api
=======
"""Initialise Flask et configure l'API Flask-RESTx"""
from flask import Flask
from flask_restx import Api
"""pip install flask-restx. Facilite la création d'API RESTful en Python """
>>>>>>> main


def create_app():
    app = Flask(__name__)
<<<<<<< HEAD
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namspacs for places, reviews, n amenities will be added later
=======
    """Créer et configurer l'application Flask."""

    api = Api(app, version='1.0', title='HBnB',
              description='HBnB Application API')
    """Initialisation de l'API Flask-RESTx"""
>>>>>>> main

    return app
