from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('main/home.html')
