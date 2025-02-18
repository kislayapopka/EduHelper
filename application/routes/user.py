from flask import Blueprint
from ..extensions import db
from ..models.user import User

# To separate different parts of routes we may use blueprints
# With blueprint we may create personal routes, like: @user.route
user = Blueprint('user', __name__)

@user.route('/user/<id>')
def create_user(id):
    user = User(id=id)
    db.session.add(user)
    db.session.commit()
    return 'User has been created!'