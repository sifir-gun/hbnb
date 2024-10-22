import sys
import os

# Ajoutez le chemin du répertoire parent pour accéder au module 'app'
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'app')))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
