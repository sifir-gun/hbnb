from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(SQLAlchemyRepository):
    """
    Dépôt pour gérer les opérations CRUD de l'entité Place.
    Hérite de SQLAlchemyRepository et utilise le modèle Place.
    """

    def __init__(self):
        super().__init__(Place)
