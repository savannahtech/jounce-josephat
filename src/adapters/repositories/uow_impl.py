from injector import inject, singleton
from sqlalchemy.orm.session import Session

from src.application.ports.repo import IRepository
from src.application.ports.uow import IUnitOfWork


@singleton
class UnitOfWork(IUnitOfWork):
    """Handles database transaction lifecycle with automatic rollbacks."""

    @inject
    def __init__(self, session: Session, repository: IRepository):
        self.session = session
        self.repository = repository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
