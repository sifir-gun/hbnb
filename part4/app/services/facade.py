from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt_identity
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place import Place
from app.models import storage
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app import db
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository


bcrypt = Bcrypt()


# Exception handler for validation errors
class ValidationError(Exception):
    pass


class HBnBFacade:
    """
    The HBnB facade enables interaction with object repositories
    (users, places, reviews, amenities).
    This class abstracts CRUD operations for multiple entities.
    """

    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def admin_update_user(self, user_id, user_data):
        """
        Admin-only method to update any user's details including email and
        password.

        Args:
            user_id (str): The ID of the user to update.
            user_data (dict): Dictionary containing the user data to update.

        Returns:
            User: The updated user object.

        Raises:
            ValueError: If user not found or email already exists.
        """
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if 'email' in user_data:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already in use")
            user.email = user_data['email']

        if 'password' in user_data:
            hashed_password = bcrypt.generate_password_hash(
                user_data['password']).decode('utf-8')
            user.password = hashed_password

        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']

        storage.save()
        return user

    def create_user(self, user_data: dict) -> User:
        """
        Create a new user.

        Args:
            user_data (dict): Dictionary containing user details.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If email is already in use or password is missing.
        """
        print("\n=== Creating User in Facade ===")
        try:
            existing_user = self.get_user_by_email(user_data.get('email'))
            if existing_user:
                raise ValueError("Email already in use")

            password = user_data.get('password')
            if not password:
                raise ValueError("Password is required")
            print("Received raw password in facade")

            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                password=password,
                is_admin=user_data.get("is_admin", False)
            )

            self.user_repo.add(user)
            print(f"User created with ID: {user.id}")
            return user

        except Exception as e:
            print(f"Error in create_user: {str(e)}")
            raise ValueError(str(e))

    def update_user(self, user_id, user_data):
        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            raise ValidationError("Unauthorized access")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValidationError("User not found")

        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']

        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValidationError("User not found")

        self.user_repo.delete(user_id)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def validate_rating(self, rating):
        """Validate that a rating is between 1 and 5"""
        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                raise ValueError
            return rating
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer between 1 and 5")

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user = storage.get(user_id)
        if not user:
            raise ValidationError(f"User with ID {user_id} not found")

        place = storage.get(place_id)
        if not place:
            raise ValidationError(f"Place with ID {place_id} not found")

        if place.owner_id == user_id:
            raise ValidationError("Owners cannot review their own place")

        existing_review = self.get_user_review_for_place(user_id, place_id)
        if existing_review:
            raise ValidationError("User has already reviewed this place")

        review = Review(
            text=review_data['text'],
            rating=self.validate_rating(review_data['rating']),
            user_id=user_id,
            place_id=place_id
        )
        storage.add(review)
        storage.save()
        return review

    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        if not name:
            raise ValidationError("Name is required")

        new_amenity = Amenity(name=name)
        storage.add(new_amenity)
        storage.save()
        return new_amenity

    def get_place(self, place_id):
        place = storage.get(place_id)
        if not place:
            raise ValidationError("Place not found")
        return place

    def create_place(self, place_data):
        self.validate_place_data(place_data)
        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        storage.add(new_place)
        storage.save()
        return new_place

    def validate_place_data(self, place_data):
        if not isinstance(place_data.get('price'), (int, float)) or not (
                1 <= place_data.get("price") <= 1000000):
            raise ValidationError(
                'Price must be a number between 1 and 1000000')
        if not isinstance(place_data.get('latitude'), (int, float)) or not (
                -90 <= place_data.get("latitude") <= 90):
            raise ValidationError(
                'Latitude must be a number between -90 and 90')
        if not isinstance(place_data.get('longitude'), (int, float)) or not (
                -180 <= place_data.get("longitude") <= 180):
            raise ValidationError(
                'Longitude must be a number between -180 and 180')
        if not isinstance(place_data.get('title'), str) or not (
                1 <= len(place_data.get("title", "")) <= 50):
            raise ValidationError('Title must be between 1 and 50 characters')
        if 'description' in place_data and not (
                1 <= len(place_data['description']) <= 500):
            raise ValidationError(
                'Description must be between 1 and 500 characters')
