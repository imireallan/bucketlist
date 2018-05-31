"""Configuration Module"""
import os

class Config(object):
    """Parent Configuration Class"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET = os.getenv("SECRET")

class DevelopmentConfig(Config):
    "Development Configuration Class"
    DEBUG = True

class ProductonConfig(Config):
    """Production Configuration Class"""
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test"

app_config = {
    "development": DevelopmentConfig,
    "production": ProductonConfig,
    "testing": TestingConfig
}