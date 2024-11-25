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
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configuration that enables debugging.

    Inherits from the base Config class and overrides settings specific to a
    development environment.
    """
    DEBUG = True


# Dictionary to manage configurations by environment
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
