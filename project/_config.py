import os

# get the folder path where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
# USERNAME = 'admin'
# PASSWORD = 'admin'

# cross site request forgery prevention
WTF_CSRF_ENABLED = True
SECRET_KEY = 'APPLES'

# set debug mode here, so that tests actually do their thang
DEBUG = False

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH