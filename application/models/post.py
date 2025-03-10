from datetime import datetime
from ..extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    caption = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=True)
    is_info = db.Column(db.Boolean, default=False)

    task_attachments = db.relationship('PostAttachment', backref='post', lazy=True)
    submissions = db.relationship('Submission', backref='post', lazy=True)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    links = db.Column(db.Text, nullable=True)

    response_attachments = db.relationship(
        'SubmissionAttachment',
        backref='submission',
        lazy=True,
        cascade="all, delete-orphan"
    )


class PostAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    file_path = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=False)


class SubmissionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
