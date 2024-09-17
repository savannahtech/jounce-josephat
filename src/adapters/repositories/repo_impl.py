import logging

from injector import inject, singleton
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from src.application.domain.benchmark import LLM, LLMBenchmarkResult, Metric
from src.application.ports.repo import IRepository

_logger = logging.getLogger(__name__)


@singleton
class Repository(IRepository):

    @inject
    def __init__(self, session: Session):
        self.session: Session = session

    def get_all_llms(self):
        return self.session.query(LLM).all()

    def get_all_metrics(self):
        return self.session.query(Metric).all()

    def get_metric_by_name(self, name):
        return self.session.query(Metric).filter(Metric.name == name).first()

    def get_llm_metric_rankings_by_metric_id(self, metric_id):
        query = (
            self.session.query(
                LLM.name,
                func.avg(LLMBenchmarkResult.value).label("mean_value"),
            )
            .join(LLMBenchmarkResult, LLM.id == LLMBenchmarkResult.llm_id)
            .filter(LLMBenchmarkResult.metric_id == metric_id)
            .group_by(LLM.name)
            .order_by(func.avg(LLMBenchmarkResult.value).desc())
        )
        results = query.all()
        return [
            {"llm": result.name, "mean_value": result.mean_value}
            for result in results
        ]

    def bulk_create_record(self, values):
        try:
            self.session.bulk_insert_mappings(LLMBenchmarkResult, values)
        except Exception as ex:
            _logger.error(ex)
            self.session.rollback()
