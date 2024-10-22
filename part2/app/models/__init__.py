"""initialise la couche de logique métier pour l'application HBnB."""
# Cette couche de logique métier définit les entités principales de
# l'application

from app.models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
