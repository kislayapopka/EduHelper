from flask import Blueprint, render_template, redirect, flash, url_for
from application import db
from application.models.user import User
from application.forms import RegistrationForm
from application.extensions import bcrypt

registration = Blueprint('registration', __name__)


@registration.route('/registration', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    patronymic=form.patronymic.data,
                    password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Регистрация была выполнена успешно!", "success")
            return redirect(url_for('login.index'))
        except Exception as e:
            print(str(e))
            flash("Ошибка регистрации.", "danger")

    return render_template('authorization/registration.html', form=form)
