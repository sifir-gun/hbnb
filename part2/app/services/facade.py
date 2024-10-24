from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place import Place


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
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Gestion des utilisateurs
    def create_user(self, user_data):
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValidationError("Email already in use")

        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
        )
        self.user_repo.add(user)
        return user

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValidationError("User not found")

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
        return user

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValidationError("User not found")
        self.user_repo.delete(user_id)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    # Gestion des reviews
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValidationError('User not found')
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValidationError('Place not found')

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_all_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValidationError("Review not found")

        if 'text' in review_data:
            review.text = review.validate_text(review_data['text'])
        if 'rating' in review_data:
            review.rating = review.validate_rating(review_data['rating'])

        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValidationError("Review not found")
        self.review_repo.delete(review_id)

    # Gestion des amenities
    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        if not name:
            raise ValidationError("Name is required")

        new_amenity = Amenity(name=name)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValidationError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValidationError("Amenity not found")

        amenity.name = amenity_data.get('name', amenity.name)
        self.amenity_repo.update(amenity_id, amenity.__dict__)
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValidationError("Amenity not found")
        self.amenity_repo.delete(amenity_id)
        return True

        # Gestion des lieux (Place)
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner'])
        if not owner:
            raise ValidationError("Owner not found")

        new_place = Place(
            title=place_data['title'],
            price=place_data['price'],
            owner=owner,
            description=place_data.get('description', ''),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude')
        )
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValidationError("Place not found")
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValidationError("Place not found")

        if 'title' in place_data:
            place.title = place.validate_title(place_data['title'])
        if 'price' in place_data:
            place.price = place.validate_price(place_data['price'])
        if 'description' in place_data:
            place.description = place_data['description']
        if 'latitude' in place_data:
            place.latitude = place.validate_latitude(place_data['latitude'])
        if 'longitude' in place_data:
            place.longitude = place.validate_longitude(place_data['longitude'])

        self.place_repo.update(place_id, place.__dict__)
        return place

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValidationError("Place not found")
        self.place_repo.delete(place_id)
        return True
