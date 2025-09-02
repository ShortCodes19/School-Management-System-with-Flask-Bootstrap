import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'something to change later')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///school.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False