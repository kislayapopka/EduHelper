from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from application.extensions import bcrypt, db
from application.forms import UserForm
from application.models.user import User

# To separate different parts of routes we may use blueprints
# With blueprint we may create personal routes, like: @admin.route
admin = Blueprint('admin', __name__)


@admin.route('/admin_panel/user_panel')
@login_required
def user_panel():
    if current_user.role != "admin":
        flash("У вас нет доступа к этой странице.", "danger")
        return redirect(url_for("feed.assignments"))

    user_form = UserForm()
    users = User.query.all()
    return render_template('admin/user_panel.html', form=user_form, users=users)


@admin.route('/admin_panel/create_user', methods=['POST'])
@login_required
def create_user():
    user_form = UserForm()

    if user_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(user_form.password.data)
        new_user = User(
            email=user_form.email.data,
            name=user_form.name.data,
            surname=user_form.surname.data,
            patronymic=user_form.patronymic.data,
            password=hashed_password,
            role=user_form.role.data
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Пользователь был успешно добавлен!", "success")
            return redirect(url_for('admin.user_panel'))
        except Exception as e:
            print(str(e))
            flash("Ошибка добавления", "danger")

    return redirect(url_for('admin.user_panel'))


@admin.route('/admin_panel/update_user', methods=['POST'])
@login_required
def update_user():
    user_id = request.form.get('id')

    if not user_id or not user_id.isdigit():
        flash("Некорректное значение ID пользователя", "danger")
        return redirect(url_for('admin.user_panel'))

    user = User.query.get(int(user_id))

    if user:
        user.name = request.form.get('name')
        user.surname = request.form.get('surname')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        db.session.commit()
        return jsonify({'message': 'Данные успешно обновлены'})
    else:
        return jsonify({'error': 'Пользователь не найден'}), 404


@admin.route('/admin_panel/get_user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'role': user.role
        })
    else:
        return jsonify({'error': 'Пользователь не найден'}), 404


@admin.route('/admin_panel/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Пользователь удалён!", "success")
    else:
        flash("Пользователь не найден!", "danger")
    return redirect(url_for('admin.user_panel'))
