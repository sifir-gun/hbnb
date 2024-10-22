"""
Ce module initialise la couche de services pour l'application HBnB.
La couche de services utilise le pattern Façade pour simplifier
l'interaction entre la logique métier et la persistance des données.
"""

from app.models.review import Review
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Classe Façade pour gérer les opérations de l'application HBnB."""

    def __init__(self):
        """Initialise les dépôts pour les utilisateurs, les lieux, les avis et les commodités."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Créer un nouvel utilisateur."""
        pass

    def get_place(self, place_id):
        """Récupérer un lieu par son ID."""
        pass

    def create_review(self, review_data):
        """Créer un nouvel avis."""
        # Valider que user_id et place_id existent
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            return None, 'User or Place not found'

        # Valider la note
        rating = review_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            return None, 'Rating must be an integer between 1 and 5'

        review = Review(**review_data)
        self.review_repo.add(review)
        return review, None

    def get_review(self, review_id):
        """Récupérer un avis par son ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Récupérer tous les avis."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Récupérer tous les avis pour un lieu spécifique."""
        return self.review_repo.get_all_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """Mettre à jour un avis existant."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Mettre à jour les attributs de l'avis
        for key, value in review_data.items():
            if key in ['text', 'rating']:
                setattr(review, key, value)
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        """Supprimer un avis."""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
