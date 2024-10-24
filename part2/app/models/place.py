from .base_model import BaseModel


class Place(BaseModel):
    """
    Représente un lieu dans l'application.

    Cette classe hérite de `BaseModel` et ajoute des fonctionnalités
    spécifiques aux objets `Place`, notamment la gestion du titre, du prix, de
    la localisation, du propriétaire, ainsi que des reviews et des amenities
    associées à ce lieu.
    """

    def __init__(self, title, price, owner, description='',
                 latitude=None, longitude=None):
        """
        Initialise un objet Place avec les attributs fournis.

        Args:
            title (str): Le titre du lieu.
            price (float): Le prix associé au lieu.
            owner (BaseModel ou int/str): Le propriétaire du lieu (soit un ID,
            soit une instance de BaseModel).
            description (str, facultatif): Une description du lieu.
            latitude (float, facultatif): La latitude du lieu.
            longitude (float, facultatif): La longitude du lieu.
        """
        # Appelle le constructeur de la classe parente `BaseModel`
        super().__init__()
        self.title = self.validate_title(title)  # Valide et assigne le titre
        self.description = description  # Description facultative
        self.price = self.validate_price(price)  # Valide et assigne le prix
        self.latitude = self.validate_latitude(
            latitude)  # Valide et assigne la latitude
        self.longitude = self.validate_longitude(
            longitude)  # Valide et assigne la longitude
        # Valide et assigne le propriétaire
        self.owner = self.validate_owner(owner)
        self.reviews = []  # Liste pour stocker les reviews associées
        self.amenities = []  # Liste pour stocker les amenities associées

    def to_dict(self):
        """
        Convertit l'objet `Place` en dictionnaire JSON-sérialisable.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'objet Place.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            # Sérialisation du propriétaire (soit ID, soit instance de
            # BaseModel)
            "owner": self.owner.id if isinstance(self.owner, BaseModel)
            else self.owner,
            # Sérialisation des reviews
            "reviews": [review.to_dict() if hasattr(review, 'to_dict')
                        else review for review in self.reviews],
            # Sérialisation des amenities
            "amenities": [amenity.to_dict() if hasattr(amenity, 'to_dict')
                          else amenity for amenity in self.amenities]
        }

    # Méthodes de validation
    def validate_title(self, title):
        """
        Valide le titre du lieu.

        Args:
            title (str): Le titre à valider.

        Returns:
            str: Le titre validé.

        Raises:
            ValueError: Si le titre est vide ou dépasse 100 caractères.
        """
        if not title or len(title) > 100:
            raise ValueError(
                "Le titre est requis et doit contenir au maximum "
                "100 caractères.")
        return title

    def validate_price(self, price):
        """
        Valide le prix du lieu.

        Args:
            price (float): Le prix à valider.

        Returns:
            float: Le prix validé.

        Raises:
            ValueError: Si le prix est inférieur ou égal à 0.
        """
        if price <= 0:
            raise ValueError("Le prix doit être un nombre positif.")
        return price

    def validate_latitude(self, latitude):
        """
        Valide la latitude du lieu.

        Args:
            latitude (float): La latitude à valider.

        Returns:
            float: La latitude validée.

        Raises:
            ValueError: Si la latitude n'est pas dans la plage valide
            [-90.0, 90.0].
        """
        if latitude is not None and (latitude < -90.0 or latitude > 90.0):
            raise ValueError(
                "La latitude doit être comprise entre -90.0 et 90.0.")
        return latitude

    def validate_longitude(self, longitude):
        """
        Valide la longitude du lieu.

        Args:
            longitude (float): La longitude à valider.

        Returns:
            float: La longitude validée.

        Raises:
            ValueError: Si la longitude n'est pas dans la plage valide
            [-180.0, 180.0].
        """
        if longitude is not None and (longitude < -180.0 or longitude > 180.0):
            raise ValueError(
                "La longitude doit être comprise entre -180.0 et 180.0.")
        return longitude

    def validate_owner(self, owner):
        """
        Valide le propriétaire du lieu.

        Args:
            owner (BaseModel, int, str): Le propriétaire à valider (soit un ID,
            soit une instance de BaseModel).

        Returns:
            BaseModel, int, str: Le propriétaire validé.

        Raises:
            ValueError: Si le propriétaire n'est pas un ID valide ou une
            instance de BaseModel.
        """
        if isinstance(owner, BaseModel):
            return owner
        elif isinstance(owner, (int, str)):  # Si le propriétaire est un ID
            return owner
        else:
            raise ValueError(
                "Le propriétaire doit être un ID ou une instance de BaseModel."
            )

    # Ajout de reviews et d'amenities
    def add_review(self, review):
        """
        Ajoute une review au lieu.

        Args:
            review: L'objet review à ajouter.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Ajoute une amenity au lieu.

        Args:
            amenity: L'objet amenity à ajouter.
        """
        self.amenities.append(amenity)
