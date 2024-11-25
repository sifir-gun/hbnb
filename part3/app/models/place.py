from app import db
from .base_model import BaseModel
from .review import Review  # Import du modèle Review
from .amenity import Amenity  # Import du modèle Amenity

# Table d'association pour Place et Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """
    Represents a place in the application.
    """

    __tablename__ = 'places'

    # Attributs
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Clé étrangère vers User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relations
    reviews_received = db.relationship("Review", back_populates="place", lazy="select")
    amenities = db.relationship("Amenity", secondary=place_amenity, lazy="subquery", backref=db.backref("places", lazy=True))
    owner = db.relationship("User", backref="places")

    def __init__(self, title, price, owner_id, description='', latitude=None, longitude=None):
        """
        Initializes a Place object.
        """
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = owner_id

    def to_dict(self):
        """
        Converts the Place object to a JSON-serializable dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.user_id,
            "reviews": [review.to_dict() for review in self.reviews_received],
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        }

    def add_review(self, review):
        """
        Adds a review to the place.
        """
        if isinstance(review, Review):
            self.reviews_received.append(review)
        else:
            raise ValueError("Invalid review object.")

    def add_amenity(self, amenity):
        """
        Adds an amenity to the place.
        """
        if isinstance(amenity, Amenity):
            self.amenities.append(amenity)
        else:
            raise ValueError("Invalid amenity object.")

    def validate_title(self, title):
        """
        Validates the title of the place.
        """
        if not title or len(title) > 100:
            raise ValueError("Title must be non-empty and less than 100 characters.")
        return title

    def validate_price(self, price):
        """
        Validates the price of the place.
        """
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return price
