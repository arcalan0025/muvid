# import logging
# logger = logging.getLogger(__name__)

# import os
# import datetime
# from flask import Flask
# from flask_migrate import Migrate
# from src.models import SQLDB, BCRYPT

# basedir = os.path.abspath(os.path.dirname(__file__))
# # App Configurations
# class CommonConfig(object):

#     # Authentication and session
#     SECRET_KEY = os.environ.get('SECRET_KEY')
#     SESSION_TYPE = 'filesystem'
#     SESSION_PERMANENT = True
#     PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=5)
#     SESSION_FILE_THRESHOLD = 500

#     # SQL-Alchemy
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

#     SQLALCHEMY_BINDS = {
#         'backend': SQLALCHEMY_DATABASE_URI,
#     }



# class DevelopmentConfig(CommonConfig):
#     """
#     Development environment configuration
#     """
#     ENV = 'development'
#     DEBUG = True
#     TESTING = False

# APP_CONFIG = {
#     'development': DevelopmentConfig,
# }

# def create_app():
#     """
#     Create a Flask application using the app factory pattern.

#     :return: Flask app
#     """
#     app = Flask(__name__)
#     app.config.from_object(DevelopmentConfig)
#     flask_env = os.getenv('FLASK_ENV')
#     if flask_env is None:
#         flask_env = 'development'
#         logger.warning("FLASK_ENV was not specified, setting to 'development' now:")
#         logger.warning("FLASK_ENV: {:}".format(flask_env))
#     else:
#         logger.info("FLASK_ENV: {:}".format(flask_env))
#     app.config.from_object(APP_CONFIG[flask_env])

#     SQLDB.init_app(app)
#     BCRYPT.init_app(app)
#     logger.info('App initialized')
#     return app

# APP = create_app()

# # Initialize Flask Migrate
# migrate = Migrate()
# migrate.init_app(APP, SQLDB)

# # API Endpoints
# from src.views.employee_view import muvid_api
# APP.register_blueprint(muvid_api, url_prefix='/api/v1/employees')

# # Run as a script
# if __name__ == '__main__':
#     if APP.config.get['ENV'] == 'development':
#         APP.run(threaded=True, port=5000)
    

# -------------------------------------------------------
# Imports
# -------------------------------------------------------

# Logging facilities
import logging
logger = logging.getLogger(__name__)

# General packages
import os
import datetime
from flask import Flask
from flask_migrate import Migrate
# SQL-Alchemy model variables
from flask_sqlalchemy import SQLAlchemy
SQLDB = SQLAlchemy()

# Sentry error logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
if os.getenv('USE_SENTRY') == 'True':
    sentry_sdk.init(
        dsn="https://10a70968bf2843a39a06561b69d34660@sentry.io/5180193",
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration(),
        ]
    )

# -------------------------------------------------------
# App configuration
# -------------------------------------------------------
class CommonConfig(object):

    # Authentication and session
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=5)
    SESSION_FILE_THRESHOLD = 500

    # SQL-Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f'postgresql://{("api_dev_user")}:{("api_dev_pass")}@{("192.168.2.242")}:{("5432")}/{("api_dev")}'

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



class ProductionConfig(CommonConfig):
    """
    Production environment configurations
    """
    ENV = 'production'
    DEBUG = False
    TESTING = False


APP_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

# -------------------------------------------------------
# Create the App
# -------------------------------------------------------
def create_app():
    # Create Flask application
    app = Flask(__name__)
    # Configure the Flask application
    flask_env = os.getenv('FLASK_ENV')
    if flask_env is None:
        flask_env = 'development'
        logger.warning("FLASK_ENV was not specified, setting to 'development' now:")
        logger.warning("FLASK_ENV: {:}".format(flask_env))
    else:
        logger.info("FLASK_ENV: {:}".format(flask_env))
    app.config.from_object(APP_CONFIG[flask_env])

    ## Initialize SQL-Alchemy support
    SQLDB.init_app(app)

    ## Initialize mail support, TODO: check if works like this
    # mail = MailSendGrid(app)
    # mail.init_app(app)
    mail = None

    logger.info("<<<<<<<<< Creating application: Finished <<<<<<<<<")
    return app

# Create the app
APP = create_app()

# -------------------------------------------------------
# API-routes
# -------------------------------------------------------
from Backend.views.employee_view import muvid_api
APP.register_blueprint(muvid_api, url_prefix='/api/v1/employees', name = 'employees')

migrate = Migrate()
migrate.init_app(APP, SQLDB)
# -------------------------------------------------------
# Run as script
# -------------------------------------------------------
if __name__ == '__main__':
    if APP.config.get('ENV') == 'development':
        ## Run threaded to avoid long TTFB waiting times in Chrome (also fixable by using Incognito mode)
        APP.run(threaded=True)
    elif APP.config.get('ENV') == 'production':
        APP.run(threaded=True)