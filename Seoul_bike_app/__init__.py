"""
# @File    :    __init__.py
# @Time    :    22/02/2022 15:54
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""
from flask import Flask


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    from Seoul_bike_app.auth.routes import auth_bp,main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app