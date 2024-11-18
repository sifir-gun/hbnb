-- test_queries.sql : Requêtes de test

-- Test d'insertion d'un lieu
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '10e92e50-1c72-43a5-8c93-a3d53b2cd8e1',
    'Cozy Cottage',
    'A nice place to relax',
    150.00,
    37.7749,
    -122.4194,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- Test de sélection
SELECT * FROM places;

-- Test de mise à jour
UPDATE places
SET price = 175.00
WHERE id = '10e92e50-1c72-43a5-8c93-a3d53b2cd8e1';

-- Test de suppression
DELETE FROM places
WHERE id = '10e92e50-1c72-43a5-8c93-a3d53b2cd8e1';
