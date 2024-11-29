# part4/models/base_model.py
from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def save(self):
        """Updates the updated_at timestamp and saves the instance."""
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Updates attributes based on the provided dictionary.
        Ensures only valid attributes are updated.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self, include_none=True):
        """
        Converts the current instance into a dictionary.
        - `include_none`: If False, omits keys with `None` values.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['created_at'] = self.created_at.isoformat() if self.created_at else None
        obj_dict['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        obj_dict.pop('_sa_instance_state', None)

        if not include_none:
            obj_dict = {k: v for k, v in obj_dict.items() if v is not None}

        return obj_dict
