from .base_model import BaseModel


class Review(BaseModel):
    """
    Classe Review représentant un avis laissé par un utilisateur pour un lieu.

    Hérite de BaseModel pour bénéficier des fonctionnalités de base comme l'ID et les méthodes 
    de gestion des objets dans le système de stockage.

    Attributs :
        text (str)   : Le texte de l'avis, requis.
        rating (int) : La note de l'avis (entre 1 et 5).
        place (obj)  : Le lieu auquel l'avis est associé, doit être une instance de Place.
        user (obj)   : L'utilisateur ayant rédigé l'avis, doit être une instance de User.

    Méthodes :
        validate_text(text)   : Valide que le texte n'est pas vide.
        validate_rating(rating) : Valide que la note est comprise entre 1 et 5.
        validate_place(place) : Valide que le lieu est une instance valide de Place.
        validate_user(user)   : Valide que l'utilisateur est une instance valide de User.
    """

    def __init__(self, text, rating, place, user):
        """
        Initialise un nouvel avis avec les attributs spécifiés.

        Args:
            text (str): Le texte de l'avis.
            rating (int): La note de l'avis (1-5).
            place (Place): Le lieu auquel l'avis est associé.
            user (User): L'utilisateur ayant rédigé l'avis.
        
        Raises:
            ValueError: Si l'un des champs 'text', 'rating', 'place' ou 'user' est invalide.
        """
        super().__init__()  # Appel au constructeur de BaseModel pour initialiser l'ID et autres
        # Validation et assignation du texte de l'avis
        self.text = self.validate_text(text)
        # Validation et assignation de la note
        self.rating = self.validate_rating(rating)
        # Validation et assignation du lieu
        self.place = self.validate_place(place)
        # Validation et assignation de l'utilisateur
        self.user = self.validate_user(user)

    def validate_text(self, text):
        """
        Valide que le texte de l'avis n'est pas vide.

        Args:
            text (str): Le texte de l'avis à valider.

        Returns:
            str: Le texte validé.

        Raises:
            ValueError: Si le texte est vide.
        """
        if not text:
            raise ValueError("Le texte de l'avis est requis.")
        return text  # Retourner le texte validé

    def validate_rating(self, rating):
        """
        Valide que la note de l'avis est comprise entre 1 et 5.

        Args:
            rating (int): La note à valider.

        Returns:
            int: La note validée.

        Raises:
            ValueError: Si la note n'est pas comprise entre 1 et 5.
        """
        if not 1 <= rating <= 5:
            raise ValueError("La note doit être comprise entre 1 et 5.")
        return rating  # Retourner la note validée

    def validate_place(self, place):
        """
        Valide que le lieu est une instance valide de Place.

        Args:
            place (Place): Le lieu à valider.

        Returns:
            Place: Le lieu validé.

        Raises:
            ValueError: Si le lieu n'est pas une instance valide de Place.
        """
        if not isinstance(place, BaseModel):
            raise ValueError("Le lieu doit être une instance valide de Place.")
        return place  # Retourner le lieu validé

    def validate_user(self, user):
        """
        Valide que l'utilisateur est une instance valide de User.

        Args:
            user (User): L'utilisateur à valider.

        Returns:
            User: L'utilisateur validé.

        Raises:
            ValueError: Si l'utilisateur n'est pas une instance valide de User.
        """
        if not isinstance(user, BaseModel):
            raise ValueError(
                "L'utilisateur doit être une instance valide de User.")
        return user  # Retourner l'utilisateur validé
