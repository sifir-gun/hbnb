from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

facade = HBnBFacade()
auth_ns = Namespace('auth', description='Authentication operations')
api = auth_ns

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate user and return a JWT token.
        The token includes user ID and admin status for authorization.
        """
        print("\n=== Login Attempt ===")
        credentials = api.payload
        print(f"Login attempt for email: {credentials.get('email')}")

        # Step 1: Get user by email
        user = facade.get_user_by_email(credentials.get('email'))
        if not user:
            print("No user found with this email")
            return {'error': 'Invalid credentials'}, 401

        print(f"Found user with email: {user.email}")

        # Step 2: Verify password
        password_valid = user.verify_password(credentials.get('password'))

        if not password_valid:
            print("Authentication failed")
            return {'error': 'Invalid credentials'}, 401

        print("Authentication successful")

        # Step 3: Generate JWT token
        identity = str(user.id)
        additional_claims = {'is_admin': user.is_admin}

        try:
            access_token = create_access_token(
                identity=identity,
                additional_claims=additional_claims
            )
            print("Token created successfully")

            return {
                'access_token': access_token,
                'is_admin': user.is_admin,
                'user_id': str(user.id)
            }, 200

        except Exception as e:
            print(f"Error creating token: {str(e)}")
            return {'error': 'Authentication error'}, 500
