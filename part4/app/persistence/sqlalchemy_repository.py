import uuid
from app import db


class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """
        Adds an object to the database. Generates a unique ID for the object if not provided.
        """
        
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Retrieves an object from the database by its ID.
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Retrieves all objects of this model from the database.
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Updates an existing object in the database with the given data.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Deletes an object from the database by its ID.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieves the first object that matches the specified attribute and value.
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
