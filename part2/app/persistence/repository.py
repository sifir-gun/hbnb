"""Référentiel en mémoire pour gérer les objets.
Fournit des méthodes pour ajouter, récupérer, mettre à jour,
et supprimer des objets."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Classe abstraite représentant un dépôt générique.
    
    Cette classe définit les méthodes de base que tout dépôt doit implémenter
    pour gérer des objets de manière générique. Elle impose l'implémentation
    de certaines méthodes via des abstractions pour gérer les objets dans un dépôt.
    """

    @abstractmethod
    def add(self, obj):
        """
        Ajoute un objet au dépôt.
        
        Args:
            obj: L'objet à ajouter au dépôt.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Récupère un objet du dépôt par son identifiant.
        
        Args:
            obj_id: L'identifiant unique de l'objet à récupérer.
        
        Returns:
            L'objet correspondant à l'identifiant donné, ou None si l'objet n'existe pas.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Récupère tous les objets du dépôt.
        
        Returns:
            Une liste contenant tous les objets du dépôt.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Met à jour un objet dans le dépôt.
        
        Args:
            obj_id: L'identifiant de l'objet à mettre à jour.
            data: Un dictionnaire contenant les nouvelles données pour l'objet.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Supprime un objet du dépôt par son identifiant.
        
        Args:
            obj_id: L'identifiant de l'objet à supprimer.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet en fonction d'un attribut spécifique.
        
        Args:
            attr_name: Le nom de l'attribut à rechercher.
            attr_value: La valeur de l'attribut pour laquelle chercher un objet.
        
        Returns:
            L'objet correspondant à la recherche, ou None s'il n'existe pas.
        """
        pass


class InMemoryRepository:
    """
    Classe représentant un dépôt en mémoire.
    
    Cette classe implémente les méthodes de base pour gérer des objets
    en mémoire, en stockant les objets dans un dictionnaire.
    """

    def __init__(self):
        """
        Initialise le dépôt avec un dictionnaire vide pour stocker les objets.
        Les objets sont stockés avec leurs ID comme clé.
        """
        self.storage = {}

    def add(self, obj):
        """
        Ajoute un objet au dépôt en utilisant son ID comme clé.
        
        Args:
            obj: L'objet à ajouter.
        """
        self.storage[obj.id] = obj

    def get(self, obj_id):
        """
        Récupère un objet par son ID depuis le dépôt.
        
        Args:
            obj_id: L'identifiant de l'objet à récupérer.
        
        Returns:
            L'objet correspondant à l'ID fourni, ou None s'il n'existe pas.
        """
        return self.storage.get(obj_id)

    def get_all(self, cls=None):
        """
        Récupère tous les objets ou tous les objets d'un type spécifique.
        
        Args:
            cls: Classe des objets à récupérer (facultatif). Si ce paramètre est fourni,
                 seuls les objets de ce type seront retournés.
        
        Returns:
            Une liste de tous les objets, ou une liste d'objets d'un certain type.
        """
        if cls is None:
            return list(self.storage.values())
        else:
            return [obj for obj in self.storage.values() if isinstance(obj, cls)]

    def update(self, obj_id, data):
        """
        Met à jour un objet existant dans le dépôt avec de nouvelles données.
        
        Args:
            obj_id: L'identifiant de l'objet à mettre à jour.
            data: Un dictionnaire contenant les nouvelles données pour l'objet.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.storage[obj_id] = obj

    def delete(self, obj_or_id):
        """
        Supprime un objet par son ID ou l'objet lui-même.
        
        Args:
            obj_or_id: L'ID de l'objet ou l'objet lui-même à supprimer.
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
        Supprime tous les objets, ou tous les objets d'un certain type.
        
        Args:
            cls: Classe des objets à supprimer (facultatif). Si ce paramètre est fourni,
                 seuls les objets de ce type seront supprimés.
        """
        if cls is None:
            self.storage.clear()
        else:
            self.storage = {
                k: v for k, v in self.storage.items() if not isinstance(v, cls)
            }

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet en fonction d'un attribut spécifique.
        
        Args:
            attr_name: Le nom de l'attribut à rechercher.
            attr_value: La valeur de l'attribut à rechercher.
        
        Returns:
            L'objet qui correspond à la recherche, ou None si aucun objet ne correspond.
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
        Récupère tous les objets qui ont un certain attribut avec une valeur donnée.
        
        Args:
            attr_name: Le nom de l'attribut à rechercher.
            attr_value: La valeur de l'attribut à rechercher.
        
        Returns:
            Une liste d'objets qui correspondent aux critères de recherche.
        """
        return [
            obj for obj in self.storage.values()
            if getattr(obj, attr_name, None) == attr_value
        ]

    def save(self):
        """
        Enregistre les changements dans le dépôt.
        Dans cette implémentation, la méthode est vide car le stockage est en mémoire,
        donc les changements sont immédiatement reflétés.
        """
        pass
