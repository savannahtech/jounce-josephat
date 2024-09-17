import os

from flask.config import Config
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

config_name = "src.infrastructure.config.settings.{}Config".format(os.environ.get("JOUNCE_ENV")) # noqa
config = Config("")
config.from_object(config_name)

db = SQLAlchemy()
migrate = Migrate()
cache_config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": config["CACHE_DEFAULT_TIMEOUT"],
    "CACHE_REDIS_HOST": config["CACHE_REDIS_HOST"],
    "CACHE_REDIS_PASSWORD": config["REDIS_PASSWORD"],
    "CACHE_REDIS_DB": config["CACHE_REDIS_DB"],
    "CACHE_KEY_PREFIX": False,
}
cache = Cache(config=cache_config)
Column = db.Column
