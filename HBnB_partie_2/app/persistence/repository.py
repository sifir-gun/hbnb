"""Référentiel en mémoire pour gérer les objets.
Fournit des méthodes pour ajouter, récupérer, mettre à jour,
et supprimer des objets."""


from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Classe abstraite représentant un dépôt générique.

    Cette classe définit les méthodes de base que tout dépôt doit implémenter
    pour gérer des objets de manière générique.
    """
    @abstractmethod
    def add(self, obj):
        """
        Ajoute un objet au dépôt.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Récupère un objet du dépôt par son identifiant.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Récupère tous les objets du dépôt.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Met à jour un objet dans le dépôt.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Supprime un objet du dépôt par son identifiant.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère des objets du dépôt par un attribut spécifique.
        """
        pass


class InMemoryRepository:
    """
    Classe représentant un dépôt en mémoire.

    Cette classe implémente les méthodes de base pour gérer des objets
    en mémoire.
    """
    def __init__(self):
        """ Un dictionnaire pour stocker les objets en mémoire,
        les clés étant les ID des objets."""
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
        """"Récupère un objet en fonction d'un attribut spécifique. exemple,
        chercher un utilisateur par son email"""
        return next(
            (
                obj for obj in self.storage.values()
                if obj.get(attr_name) == attr_value
            ),
            None
        )
