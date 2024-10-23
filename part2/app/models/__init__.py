"""initialise la couche de logique métier pour l'application HBnB.
# Cette couche de logique métier définit les entités principales de
# l'application"""

from app.persistence.repository import InMemoryRepository
storage = InMemoryRepository()