"""initializes the business logic layer for the HBnB application.
# This business logic layer defines the main entities of the
# the application"""

from app.persistence.repository import InMemoryRepository
storage = InMemoryRepository()
