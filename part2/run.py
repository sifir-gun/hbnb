from app import create_app
import sys
import os

# Ajoute le chemin du répertoire parent pour accéder au module 'app'
# Cela permet d'importer le module 'app' même si ce fichier est exécuté
# depuis un autre répertoire.
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'app')))

# Importe la fonction 'create_app' depuis le module 'app'
# Cette fonction est utilisée pour créer une instance de l'application Flask.

# Crée une instance de l'application Flask en appelant la fonction 'create_app'
app = create_app()

if __name__ == '__main__':
    """
    Ce bloc vérifie si le script est exécuté directement (et non importé
    en tant que module).
    Si c'est le cas, il lance l'application Flask avec l'option 'debug'
    activée.

    L'option 'debug=True' permet de relancer l'application automatiquement
    lors des changements de code et fournit des informations de débogage en
    cas d'erreurs.
    """
    app.run(debug=True)
