from app.models import storage
from app.models.place import Place
from app.api.v1.places import api as places_api  # L'API des places
from flask_restx import Api
from flask import Flask
import unittest
import sys
import os
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


class TestPlaceAPI(unittest.TestCase):
    def setUp(self):
        """
        Cette méthode est appelée avant chaque test.
        Elle configure l'application Flask, l'API et un client de test.
        """
        self.app = Flask(__name__)
        self.api = Api(self.app)  # Initialiser l'API
        self.api.add_namespace(places_api, path='/api/v1/places/')

        self.client = self.app.test_client()
        self.app.testing = True

        # Simuler quelques données dans le stockage
        self.place = Place(title="Maison", price=1000, owner="Xa")
        storage.add(self.place)
        storage.save()

    def tearDown(self):
        """
        Cette méthode est appelée après chaque test pour nettoyer les données.
        """
        storage.clear_all(Place)

    def test_get_places(self):
        """
        Test pour vérifier si la récupération des lieux fonctionne.
        """
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Maison', str(response.data))

    def test_post_place(self):
        """
        Test pour vérifier si la création d'un lieu fonctionne.
        """
        new_place_data = {
            'title': 'Villa',
            'price': 2000,
            'owner': 'John Doe'
        }
        response = self.client.post('/api/v1/places/', json=new_place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Villa', str(response.data))

    def test_get_place_by_id(self):
        """
        Test pour vérifier la récupération d'un lieu par son ID.
        """
        response = self.client.get(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Maison', str(response.data))

    def test_update_place(self):
        """
        Test pour vérifier si la mise à jour d'un lieu fonctionne.
        """
        update_data = {
            'title': 'Appartement'
        }
        response = self.client.put(
            f'/api/v1/places/{self.place.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Appartement', str(response.data))

    def test_delete_place(self):
        """
        Test pour vérifier si la suppression d'un lieu fonctionne.
        """
        response = self.client.delete(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Place deleted successfully', str(response.data))


if __name__ == '__main__':
    unittest.main()
