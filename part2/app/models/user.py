import re
from .base_model import BaseModel


class User(BaseModel):
    """
    Classe User représentant un utilisateur dans le système.

    Hérite de BaseModel pour bénéficier des fonctionnalités de base comme l'ID
    et les méthodes de gestion des objets dans le système de stockage.

    Attributs :
        first_name (str) : Le prénom de l'utilisateur, limité à 50 caractères.
        last_name (str)  : Le nom de famille de l'utilisateur, limité à
        50 caractères.
        email (str)      : L'adresse email de l'utilisateur, doit être une
        adresse valide.
        is_admin (bool)  : Un booléen indiquant si l'utilisateur est un
        administrateur (par défaut False).

    Méthodes :
        validate_name(name, field_name) : Valide que le nom/prénom n'est pas
        vide et contient un maximum de 50 caractères.
        validate_email(email)           : Valide que l'email est au format
        correct et est requis.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialise un nouvel utilisateur avec les attributs spécifiés.

        Args:
            first_name (str): Le prénom de l'utilisateur.
            last_name (str): Le nom de famille de l'utilisateur.
            email (str): L'adresse email de l'utilisateur.
            is_admin (bool, optional): Indique si l'utilisateur est
            administrateur (par défaut False).

        Raises:
            ValueError: Si l'un des champs 'first_name', 'last_name' ou 'email'
            est invalide.
        """
        # Appel au constructeur de BaseModel pour initialiser l'ID et autres
        super().__init__()
        # Validation et assignation du prénom
        self.first_name = self.validate_name(first_name, 'Prénom')
        # Validation et assignation du nom de famille
        self.last_name = self.validate_name(last_name, 'Nom de famille')
        # Validation et assignation de l'email
        self.email = self.validate_email(email)
        # Assignation du statut admin (par défaut False)
        self.is_admin = is_admin

    def validate_name(self, name, field_name):
        """
        Valide que le prénom ou nom de famille n'est pas vide et contient au
        maximum 50 caractères.

        Args:
            name (str): Le nom ou prénom à valider.
            field_name (str): Le nom du champ (pour personnaliser le message
            d'erreur).

        Returns:
            str: Le nom validé.

        Raises:
            ValueError: Si le nom est vide ou dépasse 50 caractères.
        """
        # Vérification si le nom est vide ou trop long
        if not name or len(name) > 50:
            raise ValueError(
                (f"{field_name} est requis et doit contenir "
                 "au maximum 50 caractères.")
            )
        return name  # Retourner le nom validé

    def validate_email(self, email):
        """
        Valide que l'email est au format valide.

        Args:
            email (str): L'adresse email à valider.

        Returns:
            str: L'email validé.

        Raises:
            ValueError: Si l'email est invalide.
        """
        # Expression régulière pour valider le format de l'email
        email_regex = r'^\S+@\S+\.\S+$'
        # Vérification si l'email est vide ou n'a pas un format correct
        if not email or not re.match(email_regex, email):
            raise ValueError("Une adresse email valide est requise.")
        # Ici, vous pourriez ajouter un contrôle d'unicité de l'email
        # dans le système de stockage
        return email  # Retourner l'email validé
