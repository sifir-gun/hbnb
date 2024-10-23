from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review


class HBnBFacade:
    """
    La façade HBnB permet d'interagir avec les dépôts d'objets utilisateurs, lieux (places), reviews et amenities.
    
    Elle sert de couche d'abstraction pour la gestion des opérations CRUD (Create, Read, Update, Delete) 
    sur les utilisateurs, les reviews, et autres entités dans le système.
    """

    def __init__(self):
        """
        Initialise les dépôts en mémoire pour les utilisateurs, les lieux (places), les reviews et les amenities.
        Chaque dépôt est représenté par un `InMemoryRepository`.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()  # Ajout d'un dépôt pour les amenities

    # Méthodes de gestion des utilisateurs

    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur après avoir vérifié que l'email n'est pas déjà utilisé.
        
        Args:
            user_data (dict): Dictionnaire contenant les informations de l'utilisateur (prénom, nom, email).
        
        Returns:
            tuple: L'utilisateur nouvellement créé et None en cas de succès, ou None et un message d'erreur.
        """
        # Vérifie si l'email est déjà utilisé
        existing_user = self.get_user_by_email(user_data['email'])
        if existing_user:
            return None, "Email already in use"

        # Crée un nouvel utilisateur
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
        )
        self.user_repo.add(user)
        return user, None

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID.
        
        Args:
            user_id (int/str): L'identifiant de l'utilisateur.
        
        Returns:
            User: L'utilisateur correspondant à l'ID, ou None s'il n'existe pas.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.
        
        Args:
            email (str): L'email de l'utilisateur.
        
        Returns:
            User: L'utilisateur correspondant à l'email, ou None s'il n'existe pas.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Récupère tous les utilisateurs stockés.
        
        Returns:
            list: Une liste de tous les utilisateurs.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Met à jour un utilisateur avec les données fournies.
        
        Args:
            user_id (int/str): L'identifiant de l'utilisateur à mettre à jour.
            user_data (dict): Les nouvelles données de l'utilisateur.
        
        Returns:
            tuple: L'utilisateur mis à jour et None en cas de succès, ou None et un message d'erreur.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None, "User not found"

        # Mise à jour des attributs de l'utilisateur
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        # Mise à jour des données de l'utilisateur
        self.user_repo.update(user_id, user.__dict__)
        return user, None

    def delete_user(self, user_id):
        """
        Supprime un utilisateur par son ID.
        
        Args:
            user_id (int/str): L'identifiant de l'utilisateur à supprimer.
        
        Returns:
            bool: True si l'utilisateur a été supprimé, False s'il n'a pas été trouvé.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    # Méthodes de gestion des reviews

    def create_review(self, review_data):
        """
        Crée une nouvelle review après avoir vérifié l'existence de l'utilisateur et du lieu associés.
        
        Args:
            review_data (dict): Les données de la review (user_id, place_id, rating, etc.).
        
        Returns:
            tuple: La review nouvellement créée et None en cas de succès, ou None et un message d'erreur.
        """
        # Valide l'existence de l'utilisateur et du lieu associés
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            return None, 'User or Place not found'

        # Valide le rating
        rating = review_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            return None, 'Rating must be an integer between 1 and 5'

        # Crée une nouvelle review
        review = Review(**review_data)
        self.review_repo.add(review)
        return review, None

    def get_review(self, review_id):
        """
        Récupère une review par son ID.
        
        Args:
            review_id (int/str): L'identifiant de la review.
        
        Returns:
            Review: La review correspondante, ou None si elle n'existe pas.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Récupère toutes les reviews stockées.
        
        Returns:
            list: Une liste de toutes les reviews.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Récupère toutes les reviews associées à un lieu spécifique.
        
        Args:
            place_id (int/str): L'identifiant du lieu.
        
        Returns:
            list: Une liste de reviews associées au lieu.
        """
        return self.review_repo.get_all_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """
        Met à jour une review avec les données fournies.
        
        Args:
            review_id (int/str): L'identifiant de la review à mettre à jour.
            review_data (dict): Les nouvelles données de la review.
        
        Returns:
            Review: La review mise à jour, ou None si elle n'a pas été trouvée.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Mise à jour des attributs de la review
        for key, value in review_data.items():
            if key in ['text', 'rating']:
                setattr(review, key, value)
        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        """
        Supprime une review par son ID.
        
        Args:
            review_id (int/str): L'identifiant de la review à supprimer.
        
        Returns:
            bool: True si la review a été supprimée, False si elle n'a pas été trouvée.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
