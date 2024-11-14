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

class ValidationError(Exception):
    """Custom exception class for validation errors in the HBnB application."""
    pass


class HBnBFacade:
    """
    Facade for interacting with repositories managing Users, Places, Reviews, and Amenities.
    This class abstracts CRUD operations across multiple entities.
    """

    def __init__(self):
        # Initialize repositories for each entity
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # -------------------- User Management --------------------

    def create_user(self, user_data: dict) -> User:
        """
        Create a new user.

        Args:
            user_data (dict): Dictionary containing user details.

        Returns:
            User: The newly created user object.
        """
        # Check if the email is already in use
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValueError("Email already in use")

        # Hash the password before saving
        password = bcrypt.generate_password_hash(user_data.get('password')).decode('utf-8')
        
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=password,  # Store the hashed password
            is_admin=user_data.get("is_admin", False)
        )
        # Add user to repository
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def delete_user(self, user_id):
        """Delete a user by ID."""
        self.user_repo.delete(user_id)

    # -------------------- Place Management --------------------

    def create_place(self, place_data: dict) -> Place:
        """
        Create a new place with provided data.

        Args:
            place_data (dict): Data needed to create a place, including title, description, etc.

        Returns:
            Place: The newly created place.
        """
        self.validate_place_data(place_data)

        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )

        # Use repository to add place
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id: int) -> Place:
        """Retrieve a place by its ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def delete_place(self, place_id):
        """Delete a place by ID."""
        self.place_repo.delete(place_id)

    # -------------------- Review Management --------------------

    def create_review(self, review_data: dict) -> Review:
        """
        Create a new review for a place.

        Args:
            review_data (dict): Data needed to create a review, including text, rating, user_id, etc.

        Returns:
            Review: The newly created review.
        """
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        # Validate user and place existence
        if not self.user_repo.get(user_id):
            raise ValidationError(f"User with ID {user_id} not found")
        if not self.place_repo.get(place_id):
            raise ValidationError(f"Place with ID {place_id} not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user_id,
            place_id=place_id
        )

        # Use repository to add review
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: int) -> Review:
        """Retrieve a review by its ID."""
        return self.review_repo.get(review_id)

    def delete_review(self, review_id: int):
        """Delete a review by its ID."""
        self.review_repo.delete(review_id)

    # -------------------- Amenity Management --------------------

    def create_amenity(self, amenity_data: dict) -> Amenity:
        """
        Create a new amenity.

        Args:
            amenity_data (dict): Data needed to create an amenity, including name.

        Returns:
            Amenity: The newly created amenity.
        """
        new_amenity = Amenity(name=amenity_data['name'])
        # Use repository to add amenity
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id: int) -> Amenity:
        """Retrieve an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id: int):
        """Delete an amenity by its ID."""
        self.amenity_repo.delete(amenity_id)

    # -------------------- Helper Methods --------------------

    def validate_place_data(self, place_data):
        """
        Validate required data for creating a place, such as title, price, latitude, etc.
        """
        if not isinstance(place_data.get('price'), (int, float)) or not (1 <= place_data.get("price") <= 1000000):
            raise ValidationError('Price must be a number between 1 and 1000000')
        if not isinstance(place_data.get('latitude'), (int, float)) or not (-90 <= place_data.get("latitude") <= 90):
            raise ValidationError('Latitude must be a number between -90 and 90')
        if not isinstance(place_data.get('longitude'), (int, float)) or not (-180 <= place_data.get("longitude") <= 180):
            raise ValidationError('Longitude must be a number between -180 and 180')
        if not isinstance(place_data.get('title'), str) or not (1 <= len(place_data.get("title", "")) <= 50):
            raise ValidationError('Title must be between 1 and 50 characters')
        if 'description' in place_data and not (1 <= len(place_data['description']) <= 500):
            raise ValidationError('Description must be between 1 and 500 characters')
