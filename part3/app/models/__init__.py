"""Initializes the business logic layer for the HBnB application.

This business logic layer defines the main entities of the application.
"""

from app.persistence.repository import InMemoryRepository
from app import db

# Table d'association Many-to-Many entre Place et Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey(
        'places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey(
        'amenities.id'), primary_key=True)
)

# Initialise l'instance de stockage
storage = InMemoryRepository()
