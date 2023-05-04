import logging
logger = logging.getLogger(__name__)

import os
import datetime
from flask import Flask
from flask_migrate import Migrate
from src.models import SQLDB, BCRYPT

# App Configurations
class CommonConfig(object):

    # Authentication and session
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=5)
    SESSION_FILE_THRESHOLD = 500

    # SQL-Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f'sqlite://{("muvid_user")}:{("muvid_pass")}@{("192.168.2.242")}:{("5432")}/{("muvid")}'

    SQLALCHEMY_BINDS = {
        'backend': SQLALCHEMY_DATABASE_URI,
    }



class DevelopmentConfig(CommonConfig):
    """
    Development environment configuration
    """
    ENV = 'development'
    DEBUG = True
    TESTING = False

def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    flask_env = os.environ.get('FLASK_ENV')
    SQLDB.init_app(app)
    BCRYPT.init_app(app)
    Migrate(app, SQLDB)
    logger.info('App initialized')
    return app

APP = create_app()

# API Endpoints
from src.views.employee_view import muvid_api
APP.register_blueprint(muvid_api, url_prefix='/api/v1/employees')

# Run as a script
if __name__ == '__main__':
    if APP.config['ENV'] == 'development':
        APP.run(threaded=True, port=5000)
    