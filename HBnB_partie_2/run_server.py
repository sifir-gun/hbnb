"""Fichier pour lancer le serveur Flask."""
from app_HBnB import create_app
from app.api.api_version1.places import app as places_app


"""Crée une instance de l'application Flask en appelant la fonction create_app()"""
app = create_app()

if __name__ == '__main__':
    """Lancer l'application en mode debug pour faciliter le développement"""
    app.run(debug=True)
