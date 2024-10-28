import pytest
from flask import Flask
from flask_restx import Api
from app.models import storage
from app.models.place import Place
from app.api.v1.places import api as places_api  # L'API des places


@pytest.fixture
def client():
    """
    Initialise l'application Flask pour les tests.
    """
    app = Flask(__name__)
    api = Api(app)
    api.add_namespace(places_api, path='/api/v1/places/')
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def setup_data():
    """
    Ajoute des données de test avant chaque test et nettoie après.
    """
    # Ajouter un lieu dans le stockage
    place = Place(title="Maison", price=1000, owner_id="Xa",
                  latitude=40.7128, longitude=-74.0060)
    storage.add(place)
    storage.save()
    yield place
    storage.clear_all(Place)


def test_get_places(client, setup_data):
    """
    Test pour vérifier la récupération des lieux.
    """
    response = client.get('/api/v1/places/')
    assert response.status_code == 200
    assert 'Maison' in response.get_data(as_text=True)


def test_post_place(client):
    """
    Test pour vérifier la création d'un lieu.
    """
    new_place_data = {
        'title': 'Villa',
        'price': 2000,
        'owner_id': 'John Doe',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'amenities': ["BBQ"]
    }
    response = client.post(
        '/api/v1/places/', json=new_place_data, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 201
    assert 'Villa' in response.get_data(as_text=True)


def test_get_place_by_id(client, setup_data):
    """
    Test pour vérifier la récupération d'un lieu par ID.
    """
    place_id = setup_data.id
    response = client.get(f'/api/v1/places/{place_id}')
    assert response.status_code == 200
    assert 'Maison' in response.get_data(as_text=True)


def test_update_place(client, setup_data):
    """
    Test pour vérifier la mise à jour d'un lieu.
    """
    place_id = setup_data.id
    update_data = {
        'title': 'Appartement',
        'price': 1500,
        'latitude': 40.7128,
        'longitude': -74.0060,
        'owner_id': 'Xa',
        'amenities': ["WiFi"]
    }
    response = client.put(
        f'/api/v1/places/{place_id}', json=update_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert 'Appartement' in response.get_data(as_text=True)


def test_delete_place(client, setup_data):
    """
    Test pour vérifier la suppression d'un lieu.
    """
    place_id = setup_data.id
    response = client.delete(f'/api/v1/places/{place_id}')
    assert response.status_code == 200
    assert 'Place deleted successfully' in response.get_data(as_text=True)
