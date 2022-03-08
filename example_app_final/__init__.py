from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        # Import Dash application

        from example_app_final.models import User
        db.create_all()
        from Bike.dash_app import init_dashboard
        app = init_dashboard(app)

    from example_app_final.main.routes import main_bp
    app.register_blueprint(main_bp)

    from example_app_final.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
