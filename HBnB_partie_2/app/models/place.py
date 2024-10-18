"""Classe Place : représente un logement dans le système.
Gère les attributs et méthodes associés aux places."""

import uuid
from datetime import datetime


class Place():
    """
    Classe représentant un lieu.

    Attributs :
    ----------
    id : str
        Identifiant unique du lieu.
    title : str
        Titre du lieu.
    description : str
        Description du lieu.
    price : float
        Prix du lieu.
    latitude : float
        Latitude géographique du lieu.
    longitude : float
        Longitude géographique du lieu.
    owner : str
        Propriétaire du lieu.
    created_at : datetime
        Date et heure de création du lieu.
    updated_at : datetime
        Date et heure de la dernière mise à jour du lieu.
    reviews : list
        Liste des avis liés à ce lieu.
    amenities : list
        Liste des équipements liés à ce lieu.
    """
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.id = str(uuid.uuid4())  # Générer un UUID unique
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reviews = []  # Liste d'avis liée à ce lie
        self.amenities = []  # Liste d'équipements liés à ce lieu

    def add_review(self, review):
        """ajoute un commentaire, un avis à ce lieu"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """ajoute un équipement à la liste à ce lieu"""
        self.amenities.append(amenity)

    def save(self):
        """Met à jour l'horloge updated_at"""
        self.updated_at = datetime.now()

    def update(self, data):
        "Met à jour les attributs du lieu"
        for key, value in data.items():

            # fonction pour vérifier si l'objet possède un attribut donné
            if hasattr(self, key):

                # fonciton pour définir dynamiquement la valeur d'un attribut.
                setattr(self, key, value)

        # met à jour l'horloge updated_at
        self.save()
