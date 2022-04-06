"""
# @File    :    __init__.py
# @Time    :    02/02/2022 13:52
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description:   The main flask app structure.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
# from flask_uploads import UploadSet, IMAGES, configure_uploads
csrf = CSRFProtect()
db = SQLAlchemy()# database

csrf._exempt_views.add('dash.dash.dispatch')

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


def create_app(config_class_name):
    """
    Creat flask app
    """

    app = Flask(__name__)

    def strf_datetime(value, strf="%Y-%m-%d %H:%M:%S"):
        return value.strftime(strf)

    app.add_template_filter(strf_datetime, "strf_datetime")

    app.config.from_object(config_class_name)
    csrf.init_app(app)
    db.init_app(app)


    login_manager.init_app(app)

    with app.app_context():
        # Import Dash application

        from seoul_bike_flask_app.models import User
        db.create_all()
        from Bike.dash_app import init_dashboard
        app = init_dashboard(app)

    from seoul_bike_flask_app.main.routes import main_bp # home page
    app.register_blueprint(main_bp)

    from seoul_bike_flask_app.auth.routes import auth_bp # other pages
    app.register_blueprint(auth_bp)

    from seoul_bike_flask_app.error_pages.handlers import error_pages # error pages
    app.register_blueprint(error_pages)

    return app
