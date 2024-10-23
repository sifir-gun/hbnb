class InMemoryRepository:
    """
    Simple in-memory repository to manage objects.
    Stores objects in a dictionary with their ID as the key.
    """

    def __init__(self):
        """ Initialize an empty storage dictionary. """
        self.storage = {}

    def add(self, obj):
        """ Add an object to the repository. """
        self.storage[obj.id] = obj  # Store the object using its ID
        return obj

    def get(self, obj_id):
        """ Get an object by its ID. """
        return self.storage.get(obj_id)

    def get_all(self):
        """ Get all objects stored in the repository. """
        return list(self.storage.values())

    def update(self, obj_id, data):
        """ Update an object with new data. """
        obj = self.get(obj_id)
        if obj:
            # Update each attribute with new data
            for key, value in data.items():
                setattr(obj, key, value)
            self.storage[obj_id] = obj

    def delete(self, obj_id):
        """ Delete an object by its ID. """
        if obj_id in self.storage:
            del self.storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """ Get an object by a specific attribute, e.g., by email. """
        for obj in self.storage.values():
            if getattr(obj, attr_name) == attr_value:
                return obj
        return None
