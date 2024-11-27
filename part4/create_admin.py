#!/usr/bin/env python3
"""Script to create an admin user"""

from app import create_app
from app.models.user import User
from app.models import storage


def create_admin():
    """Create an admin user if it doesn't exist"""
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        existing_users = storage.get_all(User)
        for user in existing_users:
            if user.email == "admin@example.com":
                print("Admin user already exists")
                return

        # Create admin user
        try:
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

        except Exception as e:
            print(f"Error creating admin: {str(e)}")


if __name__ == "__main__":
    create_admin()
