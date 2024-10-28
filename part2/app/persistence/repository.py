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
    """
    Class representing an in-memory repository.

    This class implements basic methods to manage objects in memory,
    storing them in a dictionary.
    """

    def __init__(self):
        """
        Initializes the repository with an empty dictionary to store objects.
        Objects are stored with their IDs as keys.
        """
        self.storage = {}

    def add(self, obj):
        """
        Adds an object to the repository using its ID as the key.

        Args:
            obj: The object to add.
        """
        self.storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieves an object by its ID from the repository.

        Args:
            obj_id: The identifier of the object to retrieve.

        Returns:
            The object corresponding to the provided ID,
            or None if it does not exist.
        """
        return self.storage.get(obj_id)

    def get_all(self, cls=None):
        """
        Retrieves all objects or all objects of a specific type.

        Args:
            cls: The class of objects to retrieve (optional). If provided,
            only objects of this type are returned.

        Returns:
            A list of all objects, or a list of objects of a certain type.
        """
        if cls is None:
            return list(self.storage.values())
        else:
            return [
                obj for obj in self.storage.values()
                if isinstance(obj, cls)
            ]

    def update(self, obj_id, data):
        """
        Updates an existing object in the repository with new data.

        Args:
            obj_id: The identifier of the object to update.
            data: A dictionary containing new data for the object.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.storage[obj_id] = obj

    def delete(self, obj_or_id):
        """
        Deletes an object by its ID or the object itself.

        Args:
            obj_or_id: The ID of the object or the object itself to delete.
        """
        if isinstance(obj_or_id, str):
            obj_id = obj_or_id
        elif hasattr(obj_or_id, 'id'):
            obj_id = obj_or_id.id
        else:
            raise ValueError("delete() requires a valid object or object ID")

        if obj_id in self.storage:
            del self.storage[obj_id]

    def clear_all(self, cls=None):
        """
        Deletes all objects, or all objects of a specific type.

        Args:
            cls: The class of objects to delete (optional). If provided,
            only objects of this type are deleted.
        """
        if cls is None:
            self.storage.clear()
        else:
            self.storage = {
                k: v for k, v in self.storage.items() if not isinstance(v, cls)
            }

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieves an object based on a specific attribute.

        Args:
            attr_name: The name of the attribute to search by.
            attr_value: The attribute value to match.

        Returns:
            The object that matches the search criteria,
            or None if no object matches.
        """
        return next(
            (
                obj for obj in self.storage.values()
                if getattr(obj, attr_name, None) == attr_value
            ),
            None
        )

    def get_all_by_attribute(self, attr_name, attr_value):
        """
        Retrieves all objects that have a specific attribute with a given
        value.

        Args:
            attr_name: The name of the attribute to search by.
            attr_value: The attribute value to match.

        Returns:
            A list of objects that match the search criteria.
        """
        return [
            obj for obj in self.storage.values()
            if getattr(obj, attr_name, None) == attr_value
        ]

    def save(self):
        """
        Saves changes to the repository.
        In this in-memory implementation, this method is empty because
        changes are immediately reflected.
        """
        pass
