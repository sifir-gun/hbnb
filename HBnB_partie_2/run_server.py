"""Fichier pour lancer le serveur Flask."""
from app import create_app


"""Crée une instance de l'application Flask en appelant la fonction create_app()"""
app = create_app()

if __name__ == '__main__':
    """Lancer l'application en mode debug pour faciliter le développement"""
    app.run(debug=True)
