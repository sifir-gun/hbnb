from flask import (
    Flask,
    render_template,
    Blueprint,
    abort,
    request,
    redirect,
    url_for,
    flash
)
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.models.user import User
from flask_jwt_extended import jwt_required


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """Creating and configuring the Flask application."""

    app = Flask(__name__,
                static_folder="static",
                template_folder="templates")

    # Configuration JWT plus spécifique
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_SECRET_KEY'] = 'dev-secret-key'

    # Configuration CORS plus détaillée
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5001", "http://localhost:5001"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'dev-secret-key'

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.models import init_db
    init_db(db)

    from app.models import storage
    from app.models.place import Place
    # Create main blueprint for HTML routes
    main = Blueprint('main', __name__)

    @main.route('/')
    def index():
        try:
            places = storage.get_all(Place)
            return render_template(
                'index.html', places=places if places else [])
        except Exception as e:
            print(f"Error retrieving places: {str(e)}")
            return render_template('index.html', places=[])

    @main.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            try:
                # Obtenir l'utilisateur depuis la base de données
                user = storage.get_by_attribute(User, "email", email)

                if user and user.verify_password(password):
                    # Créer un token JWT
                    token_identity = {
                        'id': str(user.id),
                        'is_admin': user.is_admin
                    }
                    access_token = create_access_token(identity=token_identity)

                    # Rediriger vers la page d'accueil
                    response = redirect(url_for('main.index'))
                    # Définir le cookie avec le token
                    response.set_cookie(
                        'token', access_token, httponly=True, secure=True
                    )
                    return response
                else:
                    flash('Email ou mot de passe incorrect')
                    return redirect(url_for('main.login'))

            except Exception as e:
                print(f"Erreur de connexion : {str(e)}")
                flash("Une erreur s'est produite lors de la connexion")
                return redirect(url_for('main.login'))

        return render_template('login.html')

    @main.route('/register')
    def register():
        return render_template('register.html')

    @main.route('/add-place')
    @jwt_required()  # Protection de la route
    def add_place():
        """Route pour ajouter un nouveau logement"""
        return render_template('add_place.html')

    @main.route('/place')
    def place_base():
        """Route pour la page de base des lieux"""
        return render_template('place.html')

    @main.route('/place/<string:place_id>')
    def place(place_id):
        """Route pour un lieu spécifique"""
        try:
            # Utiliser storage.get
            place = storage.get_all(Place)
            place = next((p for p in place if p.id == place_id), None)

            if not place:
                abort(404)  # Si la place n'existe pas
            return render_template('place.html', place=place)
        except Exception as e:
            print(f"Erreur lors de la récupération de la place : {str(e)}")
            abort(404)

    @main.route('/caravane')
    def caravane():
        return render_template('caravane.html')

    @main.route('/add_review')
    def add_review():
        return render_template('add_review.html')

    # Register the blueprint
    app.register_blueprint(main)

    # Configure REST API with Swagger
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': (
                "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'"
                "**, where JWT is the token"
            )
        }
    }

    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              authorizations=authorizations,
              security='Bearer Auth',
              doc='/api/docs')

    # Register API namespaces
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.admin import api as admin_ns

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
