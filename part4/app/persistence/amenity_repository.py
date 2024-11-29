from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.amenity import Amenity


class AmenityRepository(SQLAlchemyRepository):
    """
    Dépôt pour gérer les opérations CRUD de l'entité Amenity.
    Hérite de SQLAlchemyRepository et utilise le modèle Amenity.
    """

    def __init__(self):
        super().__init__(Amenity)
