import os

os_env = os.environ


class Config(object):
    ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    JOUNCE_ENV = "Test"
    CACHE_TYPE = "simple"
    API_KEY = os.environ.get(
        "API_KEY", "8b864ef3319545403bf7cc15b97e522dc46624780fbd6c1e9c92270d2d97c843" # noqa
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://app:app@localhost/uat_jounce"
    )
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecret")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0") # noqa
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "localhost")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    CACHE_REDIS_DB = os.environ.get("CACHE_REDIS_DB", 0)


class LocalConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "local")
    JOUNCE_ENV = "Local"


class UATConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "development")
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "redis-service")
    JOUNCE_ENV = "UAT"


class TestConfig(Config):
    ENV = os_env.get("ENV", "test")
    JOUNCE_ENV = "Test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
