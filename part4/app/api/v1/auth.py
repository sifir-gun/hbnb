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
    def post(self):
        print("\n=== Login Attempt ===")
        credentials = api.payload
        user = facade.get_user_by_email(credentials.get('email'))

        if not user or not user.verify_password(credentials.get('password')):
            return {'error': 'Invalid credentials'}, 401

        # Create token with only the necessary information
        access_token = create_access_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
