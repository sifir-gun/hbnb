from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, price, owner, description='',
                 latitude=None, longitude=None):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []
        self.amenities = []

    def validate_title(self, title):
        if not title or len(title) > 100:
            raise ValueError(
                ("Le titre est requis et doit contenir au maximum "
                 "100 caractères.")
            )
        return title

    def validate_price(self, price):
        if price <= 0:
            raise ValueError("Le prix doit être un nombre positif.")
        return price

    def validate_latitude(self, latitude):
        if latitude is not None and (latitude < -90.0 or latitude > 90.0):
            raise ValueError(
                "La latitude doit être comprise entre -90.0 et 90.0."
            )
        return latitude

    def validate_longitude(self, longitude):
        if longitude is not None and (longitude < -180.0 or longitude > 180.0):
            raise ValueError(
                "La longitude doit être comprise entre -180.0 et 180.0."
            )
        return longitude

    def validate_owner(self, owner):
        if not isinstance(owner, BaseModel):
            raise ValueError(
                "Le propriétaire doit être une instance valide de User."
            )
        return owner

    def add_review(self, review):
        """Ajoute un avis au lieu."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Ajoute une commodité au lieu."""
        self.amenities.append(amenity)
