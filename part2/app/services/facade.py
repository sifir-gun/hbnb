from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()  # Amenity repository initialized

    # User management methods
    def create_user(self, user_data):
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data['email'])
        if existing_user:
            return None, "Email already in use"

        # Create a new user
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
        )
        self.user_repo.add(user)
        return user, None

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None, "User not found"

        # Update user attributes
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        self.user_repo.update(user_id, user.__dict__)  # Update the user data
        return user, None

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    # Review management methods
    def create_review(self, review_data):
        # Validate that user_id and place_id exist
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            return None, 'User or Place not found'

        # Validate rating
        rating = review_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            return None, 'Rating must be an integer between 1 and 5'

        review = Review(**review_data)
        self.review_repo.add(review)
        return review, None

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_all_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Update review attributes
        for key, value in review_data.items():
            if key in ['text', 'rating']:
                setattr(review, key, value)

        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True

    # Amenity management methods (Added)
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
            return None, "amenity not found" # Get the amenity by ID
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None, "Amenity not found"

        # Update the name if provided
        amenity.name = amenity_data.get('name', amenity.name)
        self.amenity_repo.update(amenity_id, amenity.__dict__)  # Update the amenity data
        return amenity, None

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False, "Amenity not found"
        self.amenity_repo.delete(amenity_id)
        return True
