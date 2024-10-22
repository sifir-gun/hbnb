from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder pour créer un utilisateur
    def create_user(self, user_data):
        pass

    # Placeholder pour récupérer un lieu par ID
    def get_place(self, place_id):
        pass

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
        self.review_repo.update(review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
