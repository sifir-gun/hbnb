"""Script to run the Flask application."""
from app import create_app, db
from app.models.user import User
from app.models import storage
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Crée une instance de l'application Flask
app = create_app()


def create_admin_if_not_exists():
    """Create an admin user if it doesn't exist."""
    with app.app_context():
        # Vérifie si un administrateur existe déjà
        users = storage.get_all(User)
        admin_exists = any(user.email == "admin@example.com" for user in users)

        if not admin_exists:
            print("\n=== Creating admin user ===")
            admin = User(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                password="admin123",
                is_admin=True
            )
            storage.add(admin)
            storage.save()
            print("Admin user created successfully")
            print("Email: admin@example.com")
            print("Password: admin123")


if __name__ == '__main__':
    """
    This block is executed if the script is run directly.
    It creates the admin user if necessary and starts the Flask app.
    """
    with app.app_context():
        # Crée les tables pour tous les modèles importés
        db.create_all()
        create_admin_if_not_exists()

    # Lance l'application Flask en mode débogage
    app.run(debug=True)
