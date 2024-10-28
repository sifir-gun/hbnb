"""initializes version 1 of the API.
This API layer receives HTTP requests from users"""


from flask_restx import Api
from flask import Blueprint
from .users import api as users_api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


api = Api(api_bp, version='1.0', title='HBnB API',
          description='API for managing HBnB entities')


api.add_namespace(users_api)
