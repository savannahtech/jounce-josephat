from abc import ABC, abstractmethod

from src.application.ports.repo import IRepository


class IUnitOfWork(ABC):
    """IUnitOfWork defines an interface based on Unit of Work pattern."""

    repository: IRepository

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
