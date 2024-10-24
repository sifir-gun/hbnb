from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review


# Assuming ValidationError is defined in the same file for simplicity
class ValidationError(Exception):
    pass


class HBnBFacade:
    """
    La façade HBnB permet d'interagir avec les dépôts d'objets utilisateurs,
    lieux (places), reviews et amenities.

    Elle sert de couche d'abstraction pour la gestion des opérations CRUD
    (Create, Read, Update, Delete) sur les utilisateurs, les reviews, et
    autres entités dans le système.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Méthodes de gestion des utilisateurs

    def create_user(self, user_data):
        existing_user = self.get_user_by_email(user_data['email'])
        if existing_user:
            return None, "Email already in use"

        try:
            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
            )
            self.user_repo.add(user)
            return user, None
        except (ValueError, ValidationError) as ve:
            return None, str(ve)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None, "User not found"

        try:
            if 'first_name' in user_data:
                user.first_name = user.validate_name(
                    user_data['first_name'], 'Prénom'
                )
            if 'last_name' in user_data:
                user.last_name = user.validate_name(
                    user_data['last_name'], 'Nom de famille'
                )
            if 'email' in user_data:
                user.email = user.validate_email(user_data['email'])

            self.user_repo.update(user_id, user.__dict__)
            return user, None
        except (ValueError, ValidationError) as ve:
            return None, str(ve)

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    # Méthodes de gestion des reviews

    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            return None, 'User not found'
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            return None, 'Place not found'

        try:
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                place=place,
                user=user
            )
            self.review_repo.add(review)
            return review, None
        except (ValueError, ValidationError) as ve:
            return None, str(ve)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.

        Args:
            email (str): L'email de l'utilisateur.

        Returns:
            User: L'utilisateur correspondant à l'email, ou None s'il n'existe
            pas.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID.

        Args:
            user_id (str): L'identifiant de l'utilisateur.

        Returns:
            User: L'utilisateur correspondant à l'ID, ou None s'il n'existe pas.
        """
        return self.user_repo.get(user_id)

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None, "Review not found"

        try:
            if 'text' in review_data:
                review.text = review.validate_text(review_data['text'])
            if 'rating' in review_data:
                review.rating = review.validate_rating(review_data['rating'])

            self.review_repo.update(review_id, review.__dict__)
            return review, None
        except (ValueError, ValidationError) as ve:
            return None, str(ve)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True

    # Les autres méthodes restent inchangées
