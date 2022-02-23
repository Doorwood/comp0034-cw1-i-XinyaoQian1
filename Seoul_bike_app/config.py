"""Flask config class."""
import pathlib

"""Flask config class."""


class Config(object):
    DEBUG = False  # default setting
    SECRET_KEY = 'B_9C8Hx69an47BnynpNjCg'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(
        pathlib.Path(__file__).parent.joinpath('lab_example.sqlite'))



class ProductionConfig(Config):
    ENV = 'production'



class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True

