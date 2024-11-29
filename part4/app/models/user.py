import re
import uuid
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    # Relationships
    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='author', lazy=True)

    # Columns matching the database schema
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(255), nullable=False)  # Match schema length
    last_name = db.Column(db.String(255), nullable=False)  # Match schema length
    email = db.Column(db.String(255), unique=True, nullable=False)  # Match schema length
    password = db.Column(db.String(255), nullable=False)  # Match schema length
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a new user with validated data and hashed password."""
        self.id = str(uuid.uuid4())  # Generate UUID for id
        self.first_name = self.validate_name(first_name, 'First name')
        self.last_name = self.validate_name(last_name, 'Last name')
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.hash_password(password)
        print(f"User initialized with email: {email}")

    def hash_password(self, password):
        """Hash the password before storing."""
        if not password:
            raise ValueError("Password is required")
        print(f"Hashing password for user: {self.email}")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(f"Password hashed. Hash: {self.password[:20]}...")

    def verify_password(self, password):
        """Verify a password against the hash."""
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
        """Validate the name (first or last name)."""
        if not name or len(name) > 255:
            raise ValueError(f"{field_name} is required and must be 255 characters or fewer.")
        return name

    def validate_email(self, email):
        """Validate the email address."""
        email_regex = r'^\S+@\S+\.\S+$'
        if not email or not re.match(email_regex, email):
            raise ValueError("A valid email address is required.")
        return email
