"""Initialise Flask et configure l'API Flask-RESTx"""
from flask import Flask
from flask_restx import Api
"""pip install flask-restx. Facilite la création d'API RESTful en Python """


def create_app():
    app = Flask(__name__)
    """Créer et configurer l'application Flask."""

    api = Api(app, version='1.0', title='HBnB',
              description='HBnB Application API')
    """Initialisation de l'API Flask-RESTx"""

    return app
