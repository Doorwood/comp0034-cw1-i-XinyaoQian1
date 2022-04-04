from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

csrf = CSRFProtect()
db = SQLAlchemy()# database
csrf._exempt_views.add('dash.dash.dispatch')

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
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

    from seoul_bike_flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from seoul_bike_flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
