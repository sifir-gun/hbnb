"""Classe Amenity : représente les commodités associées aux places."""
"""Gère les attributs et méthodes liés aux amenities."""




import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name):
        """Initialisation d'un équipement avec un identifiant unique et un horodatage"""
        self.id = str(uuid.uuid4())  # Génére un ID unique et aléatoirement
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour l'horodatage apdated_at chaque fois que l'équipement est modifé """
        self.updated_at = datetime.now()

    def update(self, data):
        """Mise à jour des attributs de l'équipement"""
        for key, value in data.items():

            # hasattr: fonction pour vérifier si l'objet possède un attribut donné
            if hasattr(self, key):

                # setattr: fonciton pour définir dynamiquement la valeur d'un attribut.
                setattr(self, key, value)

        # Mettre à jour l'horloge updated_at après les modifications
        self.save()
