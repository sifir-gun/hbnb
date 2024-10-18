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
