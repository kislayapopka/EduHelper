from datetime import datetime
from application.extensions import bcrypt, db
from application.models.user import User


def init_users():
    data = [
        {
            "name": "Кирилл",
            "surname": "Камышин",
            "patronymic": "Константинович",
            "email": "admin_user@gmail.com",
            "password": "Admin0910!",
            "role": "admin"
        },

        {
            "name": "Павел",
            "surname": "Пуховин",
            "patronymic": "Петрович",
            "email": "student_user@gmail.com",
            "password": "Student0910!",
            "role": "student"
        },

        {
            "name": "Тимофей",
            "surname": "Терешин",
            "patronymic": "Тимурович",
            "email": "teacher_user@gmail.com",
            "password": "Teacher0910!",
            "role": "teacher"
        }
    ]

    for user in data:
        if not User.query.filter_by(email=user["email"]).first():
            hashed_password = bcrypt.generate_password_hash(user["password"])
            user = User(
                name=user['name'],
                surname=user['surname'],
                patronymic=user['patronymic'],
                email=user['email'],
                password=hashed_password,
                role=user['role'],
                date=datetime.now(),
                is_active=True
            )
            db.session.add(user)

    db.session.commit()
