"""Classe Amenity : représente les commodités associées aux places.
Gère les attributs et méthodes liés aux amenities."""

import uuid
from datetime import datetime


class Amenity:
    """
    Classe représentant une commodité associée à une place.

    Attributs :
    ----------
    id : str
        Identifiant unique de la commodité.
    name : str
        Nom de la commodité.
    created_at : datetime
        Date et heure de création de la commodité.
    updated_at : datetime
        Date et heure de la dernière mise à jour de la commodité.
    """
    def __init__(self, name):
        """
        Initialise une nouvelle instance de la classe Amenity.

        Paramètres :
        -----------
        name : str
            Le nom de la commodité.
        """
        self.id = str(uuid.uuid4())  # Génére un ID unique et aléatoirement
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Met à jour l'horodatage updated_at chaque fois que l'équipement est
        modifié
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """Mise à jour des attributs de l'équipement"""
        for key, value in data.items():
            # hasattr: fonction pour vérifier si l'objet possède
            # un attribut donné
            if hasattr(self, key):
                # setattr: fonction pour définir dynamiquement la valeur
                # d'un attribut.
                setattr(self, key, value)
        # Mettre à jour l'horloge updated_at après les modifications
        self.save()
