# part4/config.py
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


class DevelopmentConfig(Config):
    """
    Development configuration that enables debugging.

    Inherits from the base Config class and overrides settings specific to a
    development environment.
    """
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the base directory
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "development.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Enable SQL query logging



# Dictionary to manage configurations by environment
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
