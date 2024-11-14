from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review


class ReviewRepository(SQLAlchemyRepository):
    """
    Dépôt pour gérer les opérations CRUD de l'entité Review.
    Hérite de SQLAlchemyRepository et utilise le modèle Review.
    """

    def __init__(self):
        super().__init__(Review)
