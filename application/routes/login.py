from flask import Blueprint, render_template

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def index():
    return render_template('authorization/login.html')