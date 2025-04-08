from datetime import datetime
from application.extensions import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=True)
    patronymic = db.Column(db.String(30), nullable=True)
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    avatar = db.Column(db.String(200))
    role = db.Column(db.String(30), default='student')

    date = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    posts = db.relationship(
        'Post',
        cascade='all, delete-orphan',
        backref='author',
        lazy=True,
    )

    submissions = db.relationship(
        'Submission',
        passive_deletes=True,
        backref='student',
        lazy=True,
    )

    courses = db.relationship(
        'CourseUser',
        cascade='all, delete-orphan',
        backref='user'
    )
