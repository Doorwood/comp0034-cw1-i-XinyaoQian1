
"""
# @File    :    config.py
# @Time    :    24/03/2022 01:36
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: Flask config class
"""
import pathlib


class Config(object):
    '''
    flask app config

    '''
    SECRET_KEY = 'generate_a_secret_key'
    WTF_CSRF_SECRET_KEY = "crFAuXFCPKbKWw8JAKfnSA"
    # don't track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # set up database location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(pathlib.Path(__file__).parent.joinpath('my_example.sqlite'))
    TESTING = False




class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
