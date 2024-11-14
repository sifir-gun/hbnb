"""Script to run the Flask application."""
import sys
import os
from app import create_app, db  # Import unique de create_app et db
from app.models.user import User
from app.models import storage
# Imports des nouveaux modèles task8
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Adds the parent directory to the path to access the 'app' module
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'app')))

# Creates an instance of the Flask application
app = create_app()


def create_admin_if_not_exists():
    """Create admin user if it doesn't exist."""
    with app.app_context():
        # Check if admin already exists
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
    This block checks if the script is executed directly
    (not imported as a module).
    If so, it creates the admin user if needed and starts the
    Flask application with debugging enabled.
    """
    create_admin_if_not_exists()
    with app.app_context():
        db.create_all()  # Crée les tables pour tous les modèles importés
    app.run(debug=True)
