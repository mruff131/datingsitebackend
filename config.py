import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():  #settings
    '''
        Set config variables for the flask app
        Using Environment variables where available.
        Otherwise create the config variable if not done already
    '''

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never get access to my CSS' #makes app more secure, normally will hide this+
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    