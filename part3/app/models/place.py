from app import db
from .base_model import BaseModel

# Table d'association pour la relation plusieurs-à-plusieurs entre Place et Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """
    Represents a place in the application.

    This class inherits from `BaseModel` and adds specific functionalities
    for `Place` objects, including handling title, price, location, owner,
    and associated reviews and amenities.
    """

    __tablename__ = 'places'

    # Columns for Place attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Foreign key to reference the User (owner)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews_received = db.relationship("Review", backref="place_reviewed", lazy="select")
    amenities = db.relationship("Amenity", secondary=place_amenity, lazy="subquery", backref=db.backref("places", lazy=True))

    def __init__(self, title, price, owner_id, description='', latitude=None, longitude=None):
        """
        Initializes a Place object with the provided attributes.

        Args:
            title (str): Title of the place.
            price (float): Price associated with the place.
            owner_id (int): ID of the user who owns the place.
            description (str, optional): Description of the place.
            latitude (float, optional): Latitude of the place.
            longitude (float, optional): Longitude of the place.
        """
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.user_id = owner_id  # Assign the owner's ID

    def to_dict(self):
        """
        Converts the `Place` object to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing the attributes of the Place object.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.user_id,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        }

    # Validation methods (as previously defined)

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
