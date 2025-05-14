import os


class Config(object):
    USER = os.environ.get("POSTGRES_USER")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    HOST = os.environ.get("POSTGRES_HOST")
    PORT = os.environ.get("POSTGRES_PORT")
    DATABASE = os.environ.get("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SECRET_KEY = '1923hnsdcvs09erkjgmdsq'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/uploads'))

    pass
