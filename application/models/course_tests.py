import pytest
from flask import Flask

from ..extensions import db
from models.post import Course


@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_course(teacher_user):
    course = Course(
        code='TEST101',
        name='Test Course',
        description='Initial Description',
        teacher_id=teacher_user.id
    )
    db.session.add(course)
    db.session.commit()
    return course


def test_create_course(client, teacher_user):
    data = {
        'code': 'NEW101',
        'name': 'New Course',
        'description': 'Test Description',
        'teacher_id': teacher_user.id
    }

    response = client.post('/api/courses', json=data)
    assert response.status_code == 201
    assert response.json['code'] == 'NEW101'

    course = Course.query.filter_by(code='NEW101').first()
    assert course is not None
    assert course.name == 'New Course'


def test_duplicate_code(client, teacher_user, test_course):
    data = {
        'code': 'TEST101',
        'name': 'Duplicate Course',
        'teacher_id': teacher_user.id
    }

    response = client.post('/api/courses', json=data)
    assert response.status_code == 400
    assert 'already exists' in response.json['message']


def test_validation(client, teacher_user):
    invalid_data = [
        ({'name': '', 'teacher_id': teacher_user.id}, 'code'),
        ({'code': 'LONGCODE123', 'name': 'Test', 'teacher_id': teacher_user.id}, 'code'),
        ({'code': 'TEST102', 'teacher_id': teacher_user.id}, 'name')
    ]

    for data, field in invalid_data:
        response = client.post('/api/courses', json=data)
        assert response.status_code == 400
        assert field in response.json['errors']