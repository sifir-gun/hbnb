from app import db
from .base_model import BaseModel
from datetime import datetime

class Amenity(BaseModel):
    """
    Class representing an amenity associated with a place.

    Attributes:
    ----------
    id : int
        Unique identifier of the amenity.
    name : str
        Name of the amenity.
    created_at : datetime
        Creation date and time of the amenity.
    updated_at : datetime
        Last update date and time of the amenity.
    """

    __tablename__ = 'amenities'

    # Définir 'id' avec autoincrement pour générer automatiquement l'ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ajout d'autoincrement
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        """
        Initializes a new instance of the Amenity class.

        Parameters:
        ----------
        name : str
            The name of the amenity.
        """
        super().__init__()  # Appel du constructeur de BaseModel
        self.name = self.validate_name(name)

    def validate_name(self, name):
        """
        Validates the name of the amenity. Ensures it is not empty and does
        not exceed 100 characters.

        Parameters:
        ----------
        name : str
            The name to validate.

        Returns:
        -------
        str
            The validated name if it passes validation.

        Raises:
        ------
        ValueError
            If the name is empty or exceeds 100 characters.
        """
        if not name or len(name) > 100:
            raise ValueError(
                "The amenity name is required and must be 100 characters or fewer."
            )
        return name
