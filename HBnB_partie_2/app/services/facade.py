
class HBnBFacade:
    def __init__(self):
        self.users = {}
        self.reviews = {}
        self.places = {}
        self.current_user_id = 1
        self.current_review_id = 1
        self.current_place_id = 1

    def get_user_by_email(self, email):
        """Find a user by email."""
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None

    def create_user(self, user_data):
        """Create a new user."""
        user = {
            'id': self.current_user_id,
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email']
        }
        self.users[self.current_user_id] = user
        self.current_user_id += 1
        return user

    def get_user(self, user_id):
        """Get a user by ID."""
        return self.users.get(user_id)

    def get_all_users(self):
        """Return all users."""
        return list(self.users.values())

    def update_user(self, user_id, user_data):
        """Update user information."""
        user = self.get_user(user_id)
        if user:
            user['first_name'] = user_data.get('first_name', user['first_name'])
            user['last_name'] = user_data.get('last_name', user['last_name'])
            user['email'] = user_data.get('email', user['email'])
        return user

    def delete_user(self, user_id):
        """Delete a user."""
        if user_id in self.users:
            del self.users[user_id]


    def create_review(self, review_data):
        """Create a new review."""
        review = {
            'id': self.current_review_id,
            'review_text': review_data['review_text'],
            'rating': review_data['rating'],
            'user_id': review_data['user_id'],
            'place_id': review_data['place_id']
        }
        self.reviews[self.current_review_id] = review
        self.current_review_id += 1
        return review

    def get_review(self, review_id):
        """Get a review by ID."""
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return list(self.reviews.values())

    def update_review(self, review_id, review_data):
        """Update a review."""
        review = self.get_review(review_id)
        if review:
            review['review_text'] = review_data.get('review_text', review['review_text'])
            review['rating'] = review_data.get('rating', review['rating'])
        return review

    def delete_review(self, review_id):
        """Delete a review."""
        if review_id in self.reviews:
            del self.reviews[review_id]

    def get_place(self, place_id):
        """Get a place by ID (simulated for validation)."""
        return self.places.get(place_id)
