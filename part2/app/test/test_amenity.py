"""
Module de tests unitaires pour la classe Amenity.

Ce module contient des tests pour vérifier le bon fonctionnement de la
classe Amenity, notamment la création et la mise à jour des objets Amenity.
"""
import unittest
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from app.models.amenity import Amenity
except ImportError as e:
    print(f"Erreur d'importation : {e}")
    raise


class TestAmenity(unittest.TestCase):
    """
    Classe de test pour la classe Amenity.

    Cette classe contient des tests unitaires pour vérifier le bon
    fonctionnement de la classe Amenity, notamment la création et la mise
    à jour des objets Amenity.
    """
    def test_amenity_creation(self):
        """Test la création d'un objet Amenity."""
        amenity = Amenity(name="Wi-Fi")
        # Vérifie que le nom est bien "Wi-Fi"
        self.assertEqual(amenity.name, "Wi-Fi")
        # Vérifie que created_at est une instance de datetime
        self.assertIsInstance(amenity.created_at, datetime)
        # Vérifie que updated_at est une instance de datetime
        self.assertIsInstance(amenity.updated_at, datetime)

    def test_amenity_update(self):
        """Test la mise à jour de l'objet Amenity."""
        amenity = Amenity(name="Wi-Fi")
        amenity.update({"name": "Free Wi-Fi"})
        # Vérifie que le nom a été mis à jour correctement
        self.assertEqual(amenity.name, "Free Wi-Fi")


if __name__ == '__main__':
    unittest.main()
