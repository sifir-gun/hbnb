import re
from .base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, 'Prénom')
        self.last_name = self.validate_name(last_name, 'Nom de famille')
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    def validate_name(self, name, field_name):
        if not name or len(name) > 50:
            raise ValueError(
                (f"{field_name} est requis et doit contenir "
                 "au maximum 50 caractères.")
            )
        return name

    def validate_email(self, email):
        email_regex = r'^\S+@\S+\.\S+$'
        if not email or not re.match(email_regex, email):
            raise ValueError("Une adresse email valide est requise.")
        # Vous vérifieriez l'unicité de l'email dans votre système de stockage
        return email
