from datetime import datetime
from ..extensions import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=True)
    patronymic = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)

    avatar = db.Column(db.String(200))
    role = db.Column(db.String(30), default='student')

    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
