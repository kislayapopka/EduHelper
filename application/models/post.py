from datetime import datetime
from ..extensions import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.now())
    due_date = db.Column(db.DateTime)
    caption = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=True)
    is_info = db.Column(db.Boolean, default=False)

    post_attachments = db.relationship(
        'PostAttachment',
        backref='post',
        lazy=True,
        cascade='all, delete-orphan',
    )
    submissions = db.relationship(
        'Submission',
        backref='post',
        lazy=True,
        cascade='all, delete-orphan',
    )


class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    submitted_at = db.Column(db.DateTime, default=datetime.now())
    links = db.Column(db.Text, nullable=True)

    submission_attachments = db.relationship(
        'SubmissionAttachment',
        backref='submission',
        lazy=True,
        cascade="all, delete-orphan"
    )


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    code = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    posts = db.relationship(
        'Post',
        backref='course',
        lazy=True,
        cascade='all, delete-orphan'
    )
    course_users = db.relationship(
        'CourseUser',
        backref='course',
        lazy=True,
        cascade='all, delete-orphan'
    )


""" Relationship tables for database """


# One2Many relation table
class PostAttachment(db.Model):
    __tablename__ = 'post_attachment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)

    file_path = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=False)


# One2Many relation table
class SubmissionAttachment(db.Model):
    __tablename__ = 'submission_attachment'
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)

    file_path = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(255), nullable=False)


# One2Many relation table
class CourseUser(db.Model):
    __tablename__ = 'course_users'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
