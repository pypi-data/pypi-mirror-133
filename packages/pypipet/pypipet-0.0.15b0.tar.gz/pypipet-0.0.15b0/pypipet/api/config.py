from pypipet.core.project_context import PipetContext
from pypipet.core.shop_conn.shop_connector import ShopConnector
from datetime import timedelta
import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
#     MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
#     MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
#     MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
#         ['true', 'on', '1']
#     MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
#     FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
#     FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
#     FLASKY_ADMIN = os.environ.get('FLASKY_AD')

class Config:
    PROPAGATE_EXCEPTIONS = True
    # Flask Security
    # -----------------
    # SECRET_KEY = os.environ.get('SECRET_KEY') 
    SECRET_KEY = "for_test_only"
    SECURITY_URL_PREFIX = "/auth"
    SECURITY_USER_IDENTITY_ATTRIBUTES = ("username", "email")
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_MSG_USERNAME_NOT_PROVIDED = ("You must provide a username.", "error")

    # pypipet
    # -----------------------
    BASE_UI_URL = os.getenv("BASE_UI_URL", "/")

    API_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT_DIR = os.path.dirname(API_ROOT_DIR)

    # Flask-SQLAlchemy
    # -----------------
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-CORS
    # -----------------
    CORS_ALLOW_HEADERS = ["CONTENT-TYPE", 'X-JSON-SCHEME']

    LOG_LEVEL = 'debug'

    #JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) 
    # JWT_ACCESS_TOKEN_EXPIRES = 10  # for testing timeout
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=2) 

