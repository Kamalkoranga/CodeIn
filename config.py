import os
from dotenv import load_dotenv
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    """The above class defines configuration variables for a Python
    application, including secret key, mail server settings, database
    settings, and more.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = 'smtp-relay.sendinblue.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CODEIN_MAIL_SUBJECT_PREFIX = '[CodeIn]'
    CODEIN_MAIL_SENDER = 'CodeIn Team <team@codein.com>'
    CODEIN_ADMIN = os.environ.get('CODEIN_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """
        The function `init_app` is a placeholder function that does nothing.

        :param app: The "app" parameter is an instance of the Flask
        application. It is used to initialize and configure the Flask
        application
        """
        pass  # pass statement


class DevelopmentConfig(Config):
    """The `DevelopmentConfig` class is a configuration class for a Python
    application that enables debugging and sets the SQLALCHEMY_DATABASE_URI to
    a development database URL or a default SQLite database URL.

    Args:
        Config (): inherits from the Config class
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'data-dev.sqlite')


class TestingConfig(Config):
    """The TestingConfig class is used for configuring the application for
    testing purposes, including setting the TESTING flag to True and
    specifying the database URI.

    Args:
        Config : inherits from the Config class
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    """The `ProductionConfig` class sets the `SQLALCHEMY_DATABASE_URI`
    attribute to the value of the `DATABASE_URL` environment variable or a
    default SQLite database URI.

    Args:
        Config (_type_): inherits from the Config class
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
