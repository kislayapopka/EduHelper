import os


class Config(object):
    USER = os.environ.get("POSTGRES_USER", "venik")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD", "venik0910")
    HOST = os.environ.get("POSTGRES_HOST", "localhost")
    PORT = os.environ.get("POSTGRES_PORT", "5432")
    DATABASE = os.environ.get("POSTGRES_DB", "education-DB")

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SECRET_KEY = '1923hnsdcvs09erkjgmdsq'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    pass
