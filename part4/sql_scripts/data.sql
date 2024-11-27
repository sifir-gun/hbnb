-- data.sql : Script pour insérer les données initiales
-- Insérer un utilisateur administrateur
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$wMek5.C1ys2Vfl1xHVjFoOWKh4P4QV9B7YhRgOnH1dA1p5l9SYOj6', -- Haché pour "admin1234"
    TRUE
);

-- Insérer des commodités
INSERT INTO amenities (id, name)
VALUES
    ('1b6f59ba-b5e4-4ef9-8d15-23fa50f4a6e1', 'WiFi'),
    ('3ac1f0cb-8cbe-4421-bd3b-2fd8339c3a3f', 'Swimming Pool'),
    ('e1d23d65-0de5-4a63-93d2-f2b17d1d6a0d', 'Air Conditioning');
