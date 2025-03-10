import os

from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config

# For every new created route import needs to be added
from .routes.user import user
from .routes.home import home
from .routes.feed import feed
from .routes.login import login
from .routes.registration import registration


# Creating entry point of the project
# This function builds up whole project
def create_app(config_class=Config):
    app = Flask(__name__)

    # Install all config requirements from Config.class
    app.config.from_object(config_class)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Registration of custom routes
    # First we need to import blueprint from routes
    app.register_blueprint(user)
    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(registration)
    app.register_blueprint(feed)

    # Database image with app context
    db.init_app(app)

    # Migrate is using local database to create version of database
    # So second parameter will be db variable
    migrate.init_app(app, db)

    # Login manager settings are set in __init__.py file
    login_manager.init_app(app)
    login_manager.login_view = 'login.index'
    login_manager.login_message = 'Доступ к данному разделу сайта запрещён для пользователей, не прошедщих авторизацию'
    login_manager.login_message_category = 'info'

    # Building database
    with app.app_context():
        db.create_all()

    return app
