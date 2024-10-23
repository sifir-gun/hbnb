import re
from .base_model import BaseModel
# Assuming this is where storage is managed
from app.persistence.repository import InMemoryRepository


class User(BaseModel):
    # Assuming there's a user repository or data storage to check for unique emails
    user_repo = InMemoryRepository()

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, 'First Name')
        self.last_name = self.validate_name(last_name, 'Last Name')
        self.email = self.validate_email(email)
        self.is_admin = self.validate_is_admin(is_admin)

    def validate_name(self, name, field_name):
        """Validate that the name is not empty and doesn't exceed 50 characters."""
        if not name or len(name) > 50:
            raise ValueError(
                f"{field_name} is required and must be at most 50 characters long."
            )
        return name

    def validate_email(self, email):
        """Validate the email format and check if it is unique."""
        email_regex = r'^\S+@\S+\.\S+$'
        if not email or not re.match(email_regex, email):
            raise ValueError("A valid email address is required.")

        # Check if the email already exists in the system
        if self.user_repo.get_by_attribute('email', email):
            raise ValueError("The email is already in use by another user.")

        return email

    def validate_is_admin(self, is_admin):
        """Validate that the is_admin flag is a boolean."""
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value.")
        return is_admin

    def to_dict(self):
        """Convert the User instance to a dictionary for easy serialization."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def save(self):
        """Save the user to the repository."""
        self.user_repo.add(self)
