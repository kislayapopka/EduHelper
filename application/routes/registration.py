from flask import Blueprint, render_template, redirect, flash, url_for
from application import db
from application.models.user import User
from application.forms import RegistrationForm

registration = Blueprint('registration', __name__)


@registration.route('/registration', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    patronymic=form.patronymic.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация была выполнена успешно!", "success")
        return redirect(url_for('login.index'))
    else:
        print("Ошибка регистрации.", form.errors)
    return render_template('authorization/registration.html', form=form)
