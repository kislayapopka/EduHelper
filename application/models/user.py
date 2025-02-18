from ..extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=True)
    patronym = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(30), default='student')
    email = db.Column(db.String(30), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)