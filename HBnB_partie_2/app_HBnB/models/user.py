from utils.auth_utils import hash_password, verify_password
import uuid
from datetime import datetime

"""représente un utilisateur dans le système."""
"""Cette classe gère les attributs et méthodes associés aux utilisateurs."""


class User:
    def __init__(self, username, email, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = hash_password(password)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def check_password(self, password):
        """Check the user's password using the helper function"""
        return verify_password(self.password, password)

    def save(self):
        """Updates the `updated_at` timestamp"""
        self.updated_at = datetime.now()
