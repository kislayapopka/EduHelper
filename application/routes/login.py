from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from application.forms import LoginForm
from application.models.user import User
from application.extensions import bcrypt

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.index'))

        form.password.errors.append("Неверный email или пароль")

    return render_template('authorization/login.html', form=form)


@login.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login.index'))
