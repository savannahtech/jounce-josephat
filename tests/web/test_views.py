from http import HTTPStatus

import pytest


class TestLLMMetricsByName:

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, db, llm, metrics, testapp):
        self.db = db
        self.llm = llm
        self.metrics = metrics
        self.testapp = testapp

    def test_get_llm_metrics_by_name_with_invalid_key(self):
        res = self.testapp.get(
            "/metrics/?metric_name=TTFT",
            headers={"api-key": "invalid"},
            expect_errors=True
        )
        assert res.status_code == HTTPStatus.FORBIDDEN
        assert res.json["message"] == 'REQUEST-API-KEY-INVALID'
