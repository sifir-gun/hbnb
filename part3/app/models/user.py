import re
from .base_model import BaseModel
from flask_bcrypt import Bcrypt  # type: ignore

bcrypt = Bcrypt()


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a new user with a hashed password"""
        super().__init__()
        self.first_name = self.validate_name(first_name, 'First name')
        self.last_name = self.validate_name(last_name, 'Last name')
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.hash_password(password)
        print(f"User initialized with email: {email}")

    def hash_password(self, password):
        """Hash le mot de passe avant de le stocker"""
        if not password:
            raise ValueError("Password is required")

        print(f"Hashing password for user: {self.email}")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(f"Password hashed. Hash: {self.password[:20]}...")

    def verify_password(self, password):
        """Verify a password against the hash"""
        print("\n=== Password Verification Details ===")
        print(f"User email: {self.email}")
        print(f"Stored hash: {self.password[:20]}...")

        if not password:
            print("Error: No password provided")
            return False

        try:
            print("Attempting to verify password...")
            result = bcrypt.check_password_hash(self.password, password)
            print(f"Password verification result: {result}")
            return result
        except Exception as e:
            print(f"Error during password verification: {str(e)}")
            return False

    def validate_name(self, name, field_name):
        """Validate le nom (prénom ou nom)"""
        if not name or len(name) > 50:
            raise ValueError(
                f"{field_name} is required and must be 50 characters or fewer."
            )
        return name

    def validate_email(self, email):
        """Validate l'adresse email"""
        email_regex = r'^\S+@\S+\.\S+$'
        if not email or not re.match(email_regex, email):
            raise ValueError("A valid email address is required.")
        return email
