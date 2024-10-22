import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())  # Génère un UUID unique
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour l'horodatage updated_at."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs en fonction du dictionnaire fourni."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convertit l'instance actuelle en dictionnaire."""
        # Copie les attributs de l'objet dans un dictionnaire
        obj_dict = self.__dict__.copy()
        # Conversion des dates en chaîne ISO 8601
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
