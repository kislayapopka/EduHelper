from flask import Blueprint, render_template, redirect
from application.forms import LoginForm

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('authorization/login.html', form=form)
