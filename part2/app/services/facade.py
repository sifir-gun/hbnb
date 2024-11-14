"""
Ce module initialise la couche de services pour l'application HBnB.
La couche de services utilise le pattern Façade pour simplifier
l'interaction entre la logique métier et la persistance des données.
"""

from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place import Place
from app.models import storage

# Gestionnaire d'exceptions pour les validations


class ValidationError(Exception):
    pass


class HBnBFacade:
    """
    La façade HBnB permet d'interagir avec les dépôts d'objets (utilisateurs,
    lieux, reviews, amenities).
    Cette classe abstrait les opérations CRUD pour plusieurs entités.
    """

    def __init__(self):
        """Initialise les dépôts pour les utilisateurs, les lieux, les avis et les commodités."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------------------- Gestion des Utilisateurs ------------------

    def create_user(self, user_data):
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValidationError("Email already in use")

        # Création de l'utilisateur
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
        )
        storage.add(user)  # Utilisation de storage pour ajouter l'utilisateur
        storage.save()
        return user

    def update_user(self, user_id, user_data):
        # Récupération de l'utilisateur
        user = storage.get(user_id)
        if not user:
            raise ValidationError("User not found")

        # Mise à jour des champs de l'utilisateur
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']

        storage.save()  # Sauvegarde des changements
        return user

    def delete_user(self, user_id):
        # Récupération de l'utilisateur
        user = storage.get(user_id)
        if not user:
            raise ValidationError("User not found")
        storage.delete(user)  # Suppression de l'utilisateur
        storage.save()

    def get_user(self, user_id):
        # Récupération de l'utilisateur depuis storage
        return storage.get(user_id)

    def get_user_by_email(self, email):
        # Rechercher l'utilisateur par email dans tous les objets
        users = storage.get_all(User)
        for user in users:
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        return storage.get_all(User)  # Récupération de tous les utilisateur

    # ---------------------------- Gestion des Reviews ------------------------

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        print(f"Debug: User ID = {user_id}, Place ID = {place_id}")

        user = storage.get(user_id)
        if not user:
            print(f"Error: User {user_id} not found.")
            raise ValidationError(f"User with ID {user_id} not found")

        place = storage.get(place_id)
        if not place:
            print(f"Error: Place {place_id} not found.")
            raise ValidationError(f"Place with ID {place_id} not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user_id,
            place_id=place_id
        )
        storage.add(review)
        storage.save()
        print(f"Review created with ID: {review.id}")
        return review

    def get_review(self, review_id):
        return storage.get(review_id)

    def get_all_reviews(self):
        return storage.get_all(Review)

    def update_review(self, review_id, review_data):
        review = storage.get(review_id)
        if not review:
            raise ValidationError("Review not found")

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        storage.save()
        return review

    def delete_review(self, review_id):
        print(f"Attempting to delete review with ID: {review_id}")
        review = storage.get(review_id)
        if not review:
            print(f"Error: Review with ID {review_id} not found.")
            return {
             "message": "Review not found. It might have already been deleted."
            }, 200

        storage.delete(review)
        storage.save()
        print(f"Review with ID {review_id} successfully deleted.")
        return {"message": "Review deleted successfully"}, 200

    # ---------------------------- Gestion des Amenities ----------------------

    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        if not name:
            return None, "Name is required"

        # Create new Amenity object and save to storage
        new_amenity = Amenity(name=name)
        self.amenity_repo.add(new_amenity)
        return new_amenity, None

    def get_amenity(self, amenity_id):
        """
        Retrieves an amenity by ID from the repository.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None, "amenity not found"  # Get the amenity by ID
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None, "Amenity not found"

        # Update the name if provided
        amenity.name = amenity_data.get('name', amenity.name)
        # Update the amenity data
        self.amenity_repo.update(amenity_id, amenity.__dict__)
        return amenity, None

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False, "Amenity not found"
        self.amenity_repo.delete(amenity_id)
        return True

    # ---------------------------- Gestion des Lieux (Place) ------------------

    def create_place(self, place_data):
        # Validation des champs obligatoires
        self.validate_place_data(place_data)

        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )

        # Ajoute le lieu au stockage
        storage.add(new_place)
        storage.save()
        return new_place

    def validate_place_data(self, place_data):
        """
        Fonction interne pour valider les données d'un lieu.
        """
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

    def get_place(self, place_id):
        return self.place_repo(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        for key, value in place_data.items():
            setattr(place, key, value)

        storage.save()
        return place

    def delete_place(self, place_id):
        place = storage.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        storage.delete(place)
        storage.save()
        return {"message": "Place deleted successfully"}, 200
