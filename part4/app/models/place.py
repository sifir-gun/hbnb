from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from .base_model import BaseModel, db
from .place_amenity import place_amenity

amenities = db.relationship(
    'Amenity',
    secondary=place_amenity,
)


class Place(BaseModel, db.Model):
    """
    Represents a place in the application.

    This class inherits from `BaseModel` and adds specific functionalities
    for `Place` objects, including handling title, price, location, owner,
    and associated reviews and amenities.
    """

    __tablename__ = 'places'

    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)
    reviews = relationship('Review', backref='place', lazy=True)

    # Définir les colonnes SQLAlchemy pour chaque attribut
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), nullable=False)
    photos = db.Column(JSON, nullable=True)

    # Relation Many-to-Many avec Amenity
    amenities = db.relationship(
        'Amenity',
        secondary='place_amenity',
        back_populates='places'
    )

    def __init__(self, title, price, owner_id, description='',
                 latitude=None, longitude=None, photos=None):
        """
        Initializes a Place object with the provided attributes.

        Args:
            title (str): Title of the place.
            price (float): Price associated with the place.
            owner_id (BaseModel or int/str): Owner of the place
            (either an ID or an instance of BaseModel).
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
        self.photos = photos if photos is not None else []
        self.reviews = []  # List to store associated reviews
        self.amenities = []  # List to store associated amenities

    def to_dict(self):
        """
        Converts the `Place` object to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing the attributes of the Place object.
        """
        # Obtenez le dictionnaire de base de la classe parente
        obj_dict = super().to_dict()
        # Ajoutez ou mettez à jour les champs spécifiques à Place
        obj_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "photos": self.photos or [],
            # Sérialisation des reviews
            "reviews": [review.to_dict() for review in self.reviews],
            # Sérialisation des amenities
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        })
        # Supprimez les clés indésirables si nécessaire
        obj_dict.pop('user_id', None)  # Si 'user_id' est redondant avec 'owner_id'
        return obj_dict

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
        return title

    def validate_price(self, price):
        """
        Validates the price of the place.

        Args:
            price (float): The price to validate.

        Returns:
            float: The validated price.

        Raises:
            ValueError: If the price is less than or equal to 0.
        """
        if price <= 0:
            raise ValueError("The price must be a positive number.")
        return price

    def validate_latitude(self, latitude):
        """
        Validates the latitude of the place.

        Args:
            latitude (float): The latitude to validate.

        Returns:
            float: The validated latitude.

        Raises:
            ValueError: If the latitude is not within the valid range
            [-90.0, 90.0].
        """
        if latitude is not None and (latitude < -90.0 or latitude > 90.0):
            raise ValueError(
                "The latitude must be between -90.0 and 90.0."
            )
        return latitude

    def validate_longitude(self, longitude):
        """
        Validates the longitude of the place.

        Args:
            longitude (float): The longitude to validate.

        Returns:
            float: The validated longitude.

        Raises:
            ValueError: If the longitude is not within the valid range
            [-180.0, 180.0].
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
            owner_id (BaseModel, int, str): The owner to validate (either an
            ID or a BaseModel instance).

        Returns:
            BaseModel, int, str: The validated owner.

        Raises:
            ValueError: If the owner is not a valid ID or an instance of
            BaseModel.
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
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Adds an amenity to the place.

        Args:
            amenity: The amenity object to add.
        """
        self.amenities.append(amenity)
