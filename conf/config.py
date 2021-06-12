import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 配置文件
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "_5#y2LF4Q8z\n\xec]/_5y2LF4Q8z\n\xec]/"
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = '1988114'
    DB_DATABASE = 'library'
    ITEMS_PER_PAGE = 10
    JWT_AUTH_URL_RULE = '/api/auth'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
