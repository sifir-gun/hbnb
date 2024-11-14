from app import db
from .base_model import BaseModel


class Review(BaseModel):
    """
    Review class representing a review left by a user for a place.

    Inherits from BaseModel to gain base functionalities such as ID
    and object management methods in the storage system.

    Attributes:
        text (str): The text of the review, required.
        rating (int): The rating of the review (between 1 and 5).
        place_id (str): The ID of the place associated with the review.
        user_id (str): The ID of the user who wrote the review.

    Methods:
        validate_text(text): Validates that the text is not empty.
        validate_rating(rating): Validates that the rating is between 1 and 5.
        validate_place(place): Validates that the place is a valid instance
        of Place.
        validate_user(user): Validates that the user is a valid instance
        of User.
    """

    __tablename__ = 'reviews'

    # Définition des colonnes
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Clés étrangères
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

    # Relation avec Place
    user = db.relationship("User", backref="reviews")
    place_id = db.relationship("Place", backref="reviews")

    def __init__(self, text, rating, place_id, user_id):
        """
        Initializes a new review with the specified attributes.

        Args:
            text (str): The text of the review.
            rating (int): The rating of the review (1-5).
            place_id (str): The ID of the place associated with the review.
            user_id (str): The ID of the user who wrote the review.

        Raises:
            ValueError: If any of the 'text', 'rating', 'place_id', or
            'user_id' fields are invalid.
        """
        # Call the BaseModel constructor to initialize the ID and other
        # base attributes
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id

    def validate_text(self, text):
        """
        Validates that the review text is not empty.

        Args:
            text (str): The review text to validate.

        Returns:
            str: The validated text.

        Raises:
            ValueError: If the text is empty.
        """
        if not text:
            raise ValueError("Review text is required.")
        return text  # Return the validated text

    def validate_rating(self, rating):
        """
        Validates that the review rating is between 1 and 5.

        Args:
            rating (int): The rating to validate.

        Returns:
            int: The validated rating.

        Raises:
            ValueError: If the rating is not between 1 and 5.
        """
        print(f"Debug: Validating rating={rating} of type {type(rating)}")
        try:
            rating = int(rating)
        except ValueError:
            raise ValueError("The rating must be an integer.")

        if not 1 <= rating <= 5:
            raise ValueError("The rating must be between 1 and 5.")
        return rating

    def validate_place(self, place):
        """
        Validates that the place is a valid instance of Place.

        Args:
            place (Place): The place to validate.

        Returns:
            Place: The validated place.

        Raises:
            ValueError: If the place is not a valid instance of Place.
        """
        if not isinstance(place, BaseModel):
            raise ValueError("The place must be a valid instance of Place.")
        return place  # Return the validated place

    def validate_user(self, user):
        """
        Validates that the user is a valid instance of User.

        Args:
            user (User): The user to validate.

        Returns:
            User: The validated user.

        Raises:
            ValueError: If the user is not a valid instance of User.
        """
        if not isinstance(user, BaseModel):
            raise ValueError("The user must be a valid instance of User.")
        return user  # Return the validated user
