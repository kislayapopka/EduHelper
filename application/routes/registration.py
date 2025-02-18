from flask import Blueprint, render_template

registration = Blueprint('registration', __name__)

@registration.route('/registration', methods=['GET', 'POST'])
def index():
    return render_template('authorization/registration.html')