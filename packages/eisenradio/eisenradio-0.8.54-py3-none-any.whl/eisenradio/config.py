"""Pytest"""
"""Flask configuration."""
from os import path, environ
from dotenv import load_dotenv

script_path = path.dirname(__file__)
"""pytest loader"""
dotenv_loader = load_dotenv(path.join(script_path, 'instance', '.env'))


class Config:
    """Base config."""
    # SECRET_KEY = environ.get('SECRET_KEY')


class ProdConfig(Config):
    pass


class TestConfig(Config):
    pass
