from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.services.facade import HBnBFacade

facade = HBnBFacade()


def admin_required():
    """
    Custom decorator to check if the user has admin privileges.
    Must be used after @jwt_required() decorator.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = facade.get_user(current_user_id)

            if not user or not user.is_admin:
                return {'error': 'Admin privileges required'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def owner_or_admin_required(owner_id):
    """
    Custom decorator to check if the user is either the owner or an admin.
    Must be used after @jwt_required() decorator.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = facade.get_user(current_user_id)

            if not user:
                return {'error': 'User not found'}, 404

            if not user.is_admin and current_user_id != owner_id:
                return {'error': 'Unauthorized action'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
