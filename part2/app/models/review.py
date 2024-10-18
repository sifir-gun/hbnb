from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    def validate_text(self, text):
        if not text:
            raise ValueError("Le texte de l'avis est requis.")
        return text

    def validate_rating(self, rating):
        if not 1 <= rating <= 5:
            raise ValueError("La note doit être comprise entre 1 et 5.")
        return rating

    def validate_place(self, place):
        if not isinstance(place, BaseModel):
            raise ValueError("Le lieu doit être une instance valide de Place.")
        return place

    def validate_user(self, user):
        if not isinstance(user, BaseModel):
            raise ValueError(
                "L'utilisateur doit être une instance valide de User."
            )
        return user
