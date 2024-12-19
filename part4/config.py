import os


class Config:
    """
    Base configuration class with common settings.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = 'your_secret_key'
    DEBUG = False

    # Configuration JWT
    JWT_TOKEN_LOCATION = ['headers', 'cookies']  # Ajouter 'cookies'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_ACCESS_COOKIE_NAME = 'token'  # Ajouter cette ligne
    JWT_COOKIE_CSRF_PROTECT = False   # Ajouter cette ligne

    # Configuration CORS
    CORS_HEADERS = ['Content-Type', 'Authorization']  # Modifier cette ligne
    CORS_SUPPORTS_CREDENTIALS = True  # Ajouter cette ligne
    CORS_EXPOSE_HEADERS = ['Authorization']  # Ajouter cette ligne


class DevelopmentConfig(Config):
    """
    Development configuration that enables debugging.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration supplémentaire pour le développement
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False  # En développement
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Ajouter ces configurations CORS
    CORS_ORIGINS = ["http://127.0.0.1:5001", "http://localhost:5001"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]


# Dictionary to manage configurations by environment
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
