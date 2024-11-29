import os


class Config:
    """
    Base configuration class with common settings.

    Attributes:
        SECRET_KEY (str): Secret key for application security, retrieved from
        environment variables.
        DEBUG (bool): Flag indicating if debugging is enabled; default is
        False.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = 'your_secret_key'
    DEBUG = False

    # Configuration JWT
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_ERROR_MESSAGE_KEY = 'message'

    # Configuration CORS
    CORS_HEADERS = 'Content-Type'


class DevelopmentConfig(Config):
    """
    Development configuration that enables debugging.

    Inherits from the base Config class and overrides settings specific to a
    development environment.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration supplémentaire pour le développement
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False  # En développement, permet HTTP
    CORS_SUPPORTS_CREDENTIALS = True


# Dictionary to manage configurations by environment
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
