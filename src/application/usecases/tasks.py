from celery import shared_task

from src.adapters.repositories.database import get_session
from src.adapters.repositories.repo_impl import Repository
from src.adapters.repositories.uow_impl import UnitOfWork
from src.application.usecases.main import MetricUseCases


def initialize_usecases(session):
    """
    Flask-Injector won’t handle Celery tasks because they operate
    outside of Flask’s request context. Therefore,
    manual dependency management is required.
    """
    repository = Repository(session)
    uow = UnitOfWork(session, repository)
    return MetricUseCases(uow)


@shared_task(name=__name__ + ".refresh_rankings")
def refresh_rankings():
    session = get_session()
    usecases = initialize_usecases(session)

    usecases.generate_llm_data()
