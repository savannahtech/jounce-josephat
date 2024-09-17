import pytest

from src.application.usecases.tasks import initialize_usecases


class TestUsecases:

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, db, llm, metrics):
        self.llm = llm
        self.metrics = metrics
        self.usecases = initialize_usecases(db.session)

    def test_fetch_metrics_by_name(self):
        res = self.usecases.fetch_metric_by_name("TTFT")
        assert res.name == "TTFT"
