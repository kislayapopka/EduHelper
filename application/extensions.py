from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Initialize empty database
# Later it will be populated in __init__ file while project compiling
db = SQLAlchemy()

# Initialize empty migration module
# Later it will be populated in __init__ file while project compiling
migrate = Migrate()

# Initialize empty bcrypt module
# Later it will be used in user module
bcrypt = Bcrypt()

login_manager = LoginManager()
