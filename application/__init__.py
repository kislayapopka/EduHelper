from flask import Flask
from .extensions import db, migrate
from .config import Config

# For every new created route import needs to be added
from .routes.user import user
from .routes.home import home
from .routes.login import login
from .routes.registration import registration


# Creating entry point of the project
# This function builds up whole project
def create_app(config_class=Config):
    app = Flask(__name__)

    # Install all config requirements from Config.class
    app.config.from_object(config_class)

    # Registration of custom routes
    # First we need to import blueprint from routes
    app.register_blueprint(user)
    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(registration)

    # Database image with app context
    db.init_app(app)

    # Migrate is using local database to create version of database
    # So second parameter will be db variable
    migrate.init_app(app, db)

    # Building database
    with app.app_context():
        db.create_all()

    return app
