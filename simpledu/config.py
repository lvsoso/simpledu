#coding=utf-8

class BaseConfig(object):
    """配置基类"""
    SECRET_KEY = "secret key"
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/simpledu"

class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    pass


class TestingConfig(BaseConfig):
    """ 测试环境配置 """
    pass

configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}