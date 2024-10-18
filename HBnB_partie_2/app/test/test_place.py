import unittest
from datetime import datetime
from app.models.place import Place


class TestPlace(unittest.TestCase):

    def test_place_creation(self):
        owner = {"id": "123", "name": "John Doe"}
        place = Place(title="Beautiful House", description="A lovely house to rent",
                      price=120.5, latitude=40.7128, longitude=-74.0060, owner=owner)

        # Vérification des attributs de base
        self.assertEqual(place.title, "Beautiful House")
        self.assertEqual(place.description, "A lovely house to rent")
        self.assertEqual(place.price, 120.5)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.owner, owner)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)

        # Ajout d'un avis et vérification
        review = {"id": "001", "text": "Great place!"}
        place.add_review(review)
        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0]["text"], "Great place!")

        # Ajout d'un équipement et vérification
        amenity = {"id": "001", "name": "Wi-Fi"}
        place.add_amenity(amenity)
        self.assertEqual(len(place.amenities), 1)
        self.assertEqual(place.amenities[0]["name"], "Wi-Fi")

        # Mise à jour d'un attribut et vérification
        place.update({"price": 130.0})
        self.assertEqual(place.price, 130.0)


if __name__ == "__main__":
    unittest.main()
