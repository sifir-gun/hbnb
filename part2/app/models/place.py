from .base_model import BaseModel


class Place(BaseModel):
    """
<<<<<<< HEAD
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
=======
    Represents a place in the application.

    This class inherits from `BaseModel` and adds specific functionalities
    for `Place` objects, including handling title, price, location, owner,
    and associated reviews and amenities.
    """

    def __init__(self, title, price, owner_id, description='',
                 latitude=None, longitude=None):
        """
        Initializes a Place object with the provided attributes.

        Args:
            title (str): Title of the place.
            price (float): Price associated with the place.
            owner_id (BaseModel or int/str): Owner of the place (either an ID or an instance of BaseModel).
            description (str, optional): Description of the place.
            latitude (float, optional): Latitude of the place.
            longitude (float, optional): Longitude of the place.
        """
        # Call the parent class `BaseModel` constructor
        super().__init__()
        # Validate and assign the title
        self.title = self.validate_title(title)
        self.description = description  # Optional description
        # Validate and assign the price
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(
            latitude)  # Validate and assign latitude
        self.longitude = self.validate_longitude(
            longitude)  # Validate and assign longitude
        # Validate and assign the owner
        self.owner_id = self.validate_owner_id(owner_id)
        self.reviews = []  # List to store associated reviews
        self.amenities = []  # List to store associated amenities

    def to_dict(self):
        """
        Converts the `Place` object to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing the attributes of the Place object.
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
<<<<<<< HEAD
            # Sérialisation du propriétaire (soit ID, soit instance de
            # BaseModel)
            "owner_id": self.owner.id if isinstance(self.owner, BaseModel)
            else self.owner,
            # Sérialisation des reviews
            "reviews": [review.to_dict() if hasattr(review, 'to_dict')
                        else review for review in self.reviews],
            # Sérialisation des amenities
=======
            # Serialize the owner (either ID or BaseModel instance)
            "owner_id": self.owner_id if isinstance(self.owner_id, BaseModel)
            else self.owner_id,
            # Serialize reviews
            "reviews": [review.to_dict() if hasattr(review, 'to_dict')
                        else review for review in self.reviews],
            # Serialize amenities
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
            "amenities": [amenity.to_dict() if hasattr(amenity, 'to_dict')
                          else amenity for amenity in self.amenities]
        }

<<<<<<< HEAD
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
=======
    # Validation methods
    def validate_title(self, title):
        """
        Validates the title of the place.

        Args:
            title (str): The title to validate.

        Returns:
            str: The validated title.

        Raises:
            ValueError: If the title is empty or exceeds 100 characters.
        """
        if not title or len(title) > 100:
            raise ValueError(
                "The title is required and must be 100 characters or fewer."
            )
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
        return title

    def validate_price(self, price):
        """
<<<<<<< HEAD
        Valide le prix du lieu.

        Args:
            price (float): Le prix à valider.

        Returns:
            float: Le prix validé.

        Raises:
            ValueError: Si le prix est inférieur ou égal à 0.
=======
        Validates the price of the place.

        Args:
            price (float): The price to validate.

        Returns:
            float: The validated price.

        Raises:
            ValueError: If the price is less than or equal to 0.
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
        """
        if price <= 0:
            raise ValueError("The price must be a positive number.")
        return price

    def validate_latitude(self, latitude):
        """
<<<<<<< HEAD
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
=======
        Validates the latitude of the place.

        Args:
            latitude (float): The latitude to validate.

        Returns:
            float: The validated latitude.

        Raises:
            ValueError: If the latitude is not within the valid range [-90.0, 90.0].
        """
        if latitude is not None and (latitude < -90.0 or latitude > 90.0):
            raise ValueError(
                "The latitude must be between -90.0 and 90.0."
            )
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
        return latitude

    def validate_longitude(self, longitude):
        """
<<<<<<< HEAD
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
=======
        Validates the longitude of the place.

        Args:
            longitude (float): The longitude to validate.

        Returns:
            float: The validated longitude.

        Raises:
            ValueError: If the longitude is not within the valid range [-180.0, 180.0].
        """
        if longitude is not None and (longitude < -180.0 or longitude > 180.0):
            raise ValueError(
                "The longitude must be between -180.0 and 180.0."
            )
        return longitude

    def validate_owner_id(self, owner_id):
        """
        Validates the owner of the place.

        Args:
            owner_id (BaseModel, int, str): The owner to validate (either an ID or a BaseModel instance).

        Returns:
            BaseModel, int, str: The validated owner.

        Raises:
            ValueError: If the owner is not a valid ID or an instance of BaseModel.
        """
        if isinstance(owner_id, BaseModel):
            return owner_id
        elif isinstance(owner_id, (int, str)):  # If the owner is an ID
            return owner_id
        else:
            raise ValueError(
                "The owner must be an ID or an instance of BaseModel."
            )

    # Adding reviews and amenities
    def add_review(self, review):
        """
        Adds a review to the place.

        Args:
            review: The review object to add.
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
<<<<<<< HEAD
        Ajoute une amenity au lieu.

        Args:
            amenity: L'objet amenity à ajouter.
=======
        Adds an amenity to the place.

        Args:
            amenity: The amenity object to add.
>>>>>>> b116b12ffdbc6613470b69a774bb93605b29da77
        """
        self.amenities.append(amenity)
