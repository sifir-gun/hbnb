from app import db
from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Class representing an amenity associated with a place.

    Attributes:
    ----------
    id : str
        Unique identifier of the amenity.
    name : str
        Name of the amenity.
    created_at : datetime
        Creation date and time of the amenity.
    updated_at : datetime
        Last update date and time of the amenity.
    """

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        """
        Initializes a new instance of the Amenity class.

        Parameters:
        ----------
        name : str
            The name of the amenity.
        """
        super().__init__()  # Call to the BaseModel constructor
        self.name = self.validate_name(name)

    def validate_name(self, name):
        """
        Validates the name of the amenity. Ensures it is not empty and does
        not exceed 50 characters.

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
            If the name is empty or exceeds 50 characters.
        """
        if not name or len(name) > 50:
            raise ValueError(
                "The amenity name is required and must be 50 characters or "
                "fewer."
            )
        return name
