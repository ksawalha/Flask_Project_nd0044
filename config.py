import os
SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///fyyurapp.db'

