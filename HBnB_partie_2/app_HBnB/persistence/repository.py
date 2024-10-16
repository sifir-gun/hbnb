"""Référentiel en mémoire pour gérer les objets."""
"""Fournit des méthodes pour ajouter, récupérer, mettre à jour, et supprimer des objets."""




from abc import ABC, abstractmethod
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository:
    def __init__(self):
        """ Un dictionnaire pour stocker les objets en mémoire, les clés étant les ID des objets."""
        self.storage = {}

    def add(self, obj):
        """Add un objet au référentiel."""
        self.storage[obj['id']] = obj

    def get(self, obj_id):
        """Récupère un objet par son ID"""
        return self.storage.get(obj_id)

    def get_all(self):
        """Récupère tout les objets stockés"""
        return list(self.storage.values())

    def update(self, obj_id, data):
        """Met à jour un objet avec de nouvelles données"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            self.storage[obj_id] = obj

    def delete(self, obj_id):
        """Supprime un objet par son ID"""
        if obj_id in self.storage:
            del self.storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """"Récupère un objet en fonction d'un attribut spécifique. exemple, chercher un utilisateur par son email"""
        return next((obj for obj in self.storage.values() if obj.get(attr_name) == attr_value), None)
