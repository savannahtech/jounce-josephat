import logging
import os
import sys

from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api
from injector import Binder, singleton
from sqlalchemy.orm import Session

from src.adapters.repositories.database import get_session
from src.adapters.repositories.repo_impl import Repository
from src.adapters.repositories.uow_impl import UnitOfWork
from src.adapters.web.blueprints import visualize_blueprint
from src.adapters.web.views import HealthBase, LLMMetricsByName, RankLLMMetricsAll
from src.application.ports.repo import IRepository
from src.application.ports.uow import IUnitOfWork
from src.application.ports.usecases import IUseCases
from src.application.usecases.main import MetricUseCases
from src.infrastructure.config.celery import make_celery
from src.infrastructure.config.settings import LocalConfig, TestConfig, UATConfig
from src.infrastructure.utils.extensions import cache, db, migrate


def configure(binder: Binder):
    """
    Handles dependency injection configuration.
    Here we bind interfaces to their implementations.
    """
    session = get_session()
    binder.bind(Session, to=session, scope=singleton)
    binder.bind(IRepository, to=Repository, scope=singleton)
    binder.bind(IUnitOfWork, to=UnitOfWork, scope=singleton)
    binder.bind(IUseCases, to=MetricUseCases, scope=singleton)


def create_app(config_object):
    app = Flask(
        __name__,
    )
    app.config.from_object(config_object)
    api = Api(app)

    register_extensions(app)
    register_blueprints(app)
    register_restful(api)
    configure_logger(app)
    FlaskInjector(app=app, modules=[configure])

    return app


def register_extensions(app):
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(visualize_blueprint)
    return None


def register_restful(api):
    api.add_resource(HealthBase, "/health/")
    api.add_resource(LLMMetricsByName, "/metrics/")
    api.add_resource(RankLLMMetricsAll, "/metrics/all/")


def configure_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


env = os.environ.get("JOUNCE_ENV").lower()
if env == "local":
    app = create_app(LocalConfig)
elif env == "uat":
    app = create_app(UATConfig)
else:
    app = create_app(TestConfig)

celery = make_celery(app)
