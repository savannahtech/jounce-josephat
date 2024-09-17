from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from src.application.domain.benchmark import LLM, Metric
from src.infrastructure.utils.extensions import db


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class MetricFactory(BaseFactory):
    name = Sequence(lambda n: f"gpt{n}")

    class Meta:
        model = Metric


class LLMFactory(BaseFactory):
    name = Sequence(lambda n: f"gpt{n}")

    class Meta:
        model = LLM
