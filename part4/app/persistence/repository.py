"""
In-memory repository to manage objects.
Provides methods to add, retrieve, update, and delete objects.
"""

from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract class representing a generic repository.

    This class defines basic methods that any repository should implement
    to manage objects in a generic way. It enforces the implementation
    of specific methods through abstractions to manage objects in a repository.
    """

    @abstractmethod
    def add(self, obj):
        """
        Adds an object to the repository.

        Args:
            obj: The object to add to the repository.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieves an object from the repository by its identifier.

        Args:
            obj_id: The unique identifier of the object to retrieve.

        Returns:
            The object corresponding to the given identifier,
            or None if the object does not exist.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieves all objects from the repository.

        Returns:
            A list containing all objects in the repository.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Updates an object in the repository.

        Args:
            obj_id: The identifier of the object to update.
            data: A dictionary containing new data for the object.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Deletes an object from the repository by its identifier.

        Args:
            obj_id: The identifier of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieves an object based on a specific attribute.

        Args:
            attr_name: The name of the attribute to search by.
            attr_value: The attribute value to match.

        Returns:
            The object matching the search criteria,
            or None if it does not exist.
        """
        pass


class InMemoryRepository:
    """In-memory repository implementation."""

    def __init__(self):
        """Initialize empty storage."""
        self.storage = {}
        print("New InMemoryRepository instance created")

    def add(self, obj):
        """Add object to storage."""
        print("\n=== Adding object to storage ===")
        print(f"Object ID: {obj.id}")
        print(f"Object type: {type(obj).__name__}")

        self.storage[obj.id] = obj
        print(f"Current storage keys: {list(self.storage.keys())}")

    def get(self, obj_id):
        """Get object by ID."""
        print("\n=== Getting object from storage ===")
        print(f"Searching for ID: {obj_id}")
        print(f"Available IDs: {list(self.storage.keys())}")

        obj = self.storage.get(obj_id)
        print(f"Found object: {obj is not None}")
        if obj:
            print(f"Object type: {type(obj).__name__}")

        return obj

    def get_all(self, cls=None):
        """Get all objects, optionally filtered by class."""
        print("\n=== Getting all objects ===")
        print(f"Filter class: {cls.__name__ if cls else 'None'}")

        if cls is None:
            items = list(self.storage.values())
        else:
            items = [
                obj for obj in self.storage.values()
                if isinstance(obj, cls)
            ]

        print(f"Found {len(items)} items")
        return items

    def update(self, obj_id, data):
        """Update object attributes."""
        print("\n=== Updating object ===")
        print(f"Object ID: {obj_id}")
        print(f"Update data: {data}")

        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.storage[obj_id] = obj
            print("Object updated successfully")

    def delete(self, obj_or_id):
        """Delete object from storage."""
        print("\n=== Deleting object ===")

        if isinstance(obj_or_id, str):
            obj_id = obj_or_id
            print(f"Deleting by ID: {obj_id}")
        elif hasattr(obj_or_id, 'id'):
            obj_id = obj_or_id.id
            print(f"Deleting by object ID: {obj_id}")
        else:
            raise ValueError("delete() requires a valid object or object ID")

        if obj_id in self.storage:
            del self.storage[obj_id]
            print("Object deleted successfully")
        else:
            print("Object not found")

    def clear_all(self, cls=None):
        """Clear storage, optionally by class."""
        print("\n=== Clearing storage ===")
        print(f"Filter class: {cls.__name__ if cls else 'None'}")

        if cls is None:
            self.storage.clear()
        else:
            self.storage = {
                k: v for k, v in self.storage.items()
                if not isinstance(v, cls)
            }
        print(f"Remaining items: {len(self.storage)}")

    def get_by_attribute(self, attr_name, attr_value):
        """Find first object by attribute value."""
        print("\n=== Getting object by attribute ===")
        print(f"Attribute: {attr_name}")
        print(f"Value: {attr_value}")

        try:
            obj = next(
                (obj for obj in self.storage.values()
                    if getattr(obj, attr_name, None) == attr_value),
                None
            )
            print(f"Found object: {obj is not None}")
            return obj
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def get_all_by_attribute(self, attr_name, attr_value):
        """Find all objects by attribute value."""
        print("\n=== Getting all objects by attribute ===")
        print(f"Attribute: {attr_name}")
        print(f"Value: {attr_value}")

        items = [
            obj for obj in self.storage.values()
            if getattr(obj, attr_name, None) == attr_value
        ]
        print(f"Found {len(items)} items")
        return items

    def save(self):
        """Persist changes (no-op for in-memory storage)."""
        print("\n=== Saving changes ===")
        print(f"Current storage size: {len(self.storage)}")
