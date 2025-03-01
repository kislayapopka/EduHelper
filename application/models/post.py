from datetime import datetime
from ..extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    caption = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=True)
