from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Create extensions
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """Creating and configuring the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set JWT secret key
    app.config['JWT_SECRET_KEY'] = 'dev-secret-key'

    # Initialize extensions
    CORS(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Configure authorization for Swagger UI
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': (
                "Type in the *'Value'* input box below: "
                "**'Bearer &lt;JWT&gt;'**, where JWT is the token"
            )
        }
    }

    # Create API with authorization configuration
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    # Import blueprints/namespaces
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.admin import api as admin_ns

    # Register namespaces
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
