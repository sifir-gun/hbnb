import uuid
from datetime import datetime


"""Classe Review : représente un avis laissé par un utilisateur sur un place."""
"""Gère les attributs et méthodes associés aux reviews."""


class Review:
    def __init__(self, user_id, place_id, content, rating):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.place_id = place_id
        self.content = content
        self.rating = self.validate_rating(rating)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def validate_rating(self, rating):
        """Ensures the rating is within the allowed range (1 to 5)."""
        if 1 <= rating <= 5:
            return rating
        else:
            raise ValueError("Rating must be between 1 and 5")

    def update(self, content=None, rating=None):
        """Updates the review's attributes in a simple and explicit way."""
        if content:
            self.content = content
        if rating is not None:
            self.rating = self.validate_rating(rating)

        self.updated_at = datetime.now()

    def save(self):
        """Updates the `updated_at` timestamp without changing any other data."""
        self.updated_at = datetime.now()
