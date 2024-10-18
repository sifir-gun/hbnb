from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Classe représentant une commodité associée à une place.

    Attributs :
    ----------
    id : str
        Identifiant unique de la commodité.
    name : str
        Nom de la commodité.
    created_at : datetime
        Date et heure de création de la commodité.
    updated_at : datetime
        Date et heure de la dernière mise à jour de la commodité.
    """
    def __init__(self, name):
        """
        Initialise une nouvelle instance de la classe Amenity.

        Paramètres :
        -----------
        name : str
            Le nom de la commodité.
        """
        super().__init__()  # Appel au constructeur de BaseModel
        self.name = self.validate_name(name)

    def validate_name(self, name):
        if not name or len(name) > 50:
            raise ValueError(
                "Le nom de la commodité est requis et doit contenir "
                "au maximum 50 caractères."
            )
        return name
