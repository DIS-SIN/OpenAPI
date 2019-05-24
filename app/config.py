import os

base_dir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:password@localhost/'
database_name = 'openapi'


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESOURCES_PER_PAGE = 4


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postgres_local_base + database_name)