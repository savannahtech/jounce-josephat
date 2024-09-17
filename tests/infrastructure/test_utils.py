from unittest.mock import patch

import pytest

from src.application.domain.benchmark import LLM, Metric
from src.infrastructure.utils.constants import NUMBER_OF_DATA_POINTS, SEED_VALUE
from src.infrastructure.utils.exceptions import AuthenticationException
from src.infrastructure.utils.helpers import (generate_data, generate_random_value,
                                              validate_api_key)


class TestValidateAPIKey:
    def test_validate_api_key_no_api_key(self):
        with pytest.raises(AuthenticationException, match="REQUEST-API-KEY-INVALID"): # noqa
            validate_api_key("valid_key", None, "REQUEST-API-KEY-INVALID")

    def test_validate_api_key_invalid_api_key(self):
        with pytest.raises(AuthenticationException, match="REQUEST-API-KEY-INVALID"): # noqa
            validate_api_key("valid_key", "invalid_key", "REQUEST-API-KEY-INVALID") # noqa

    def test_validate_api_key_valid_api_key(self):
        try:
            validate_api_key("valid_key", "valid_key", "REQUEST-API-KEY-INVALID") # noqa
        except AuthenticationException:
            pytest.fail("Unexpected AuthenticationException raised")


class TestGenerateRandomValues:
    def test_generate_random_value_with_invalid_metric(self):
        with pytest.raises(ValueError, match="A valid Metric object must be provided"): # noqa
            generate_random_value(None)

    def test_generate_random_value_with_no_defined_range(self):
        invalid_metric = Metric(name="test_metric", min_value=None, max_value=None) # noqa
        with pytest.raises(
            ValueError, match="Metric test_metric has no defined range."
        ):
            generate_random_value(invalid_metric)

    def test_generate_random_value_with_valid_metric(self):
        valid_metric = Metric(name="test_metric", min_value=1.0, max_value=5.0)
        random_value = generate_random_value(valid_metric)
        assert 1.0 <= random_value <= 5.0


class TestGenerateData:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, db, llm, metrics):
        self.db = db

    @patch("src.infrastructure.utils.helpers.generate_random_value")
    def test_generate_data(self, mock_generate_random_value):
        mock_generate_random_value.return_value = 3.5
        models = self.db.session.query(LLM).all()
        metrics = self.db.session.query(Metric).all()
        data = generate_data(
            seed=SEED_VALUE,
            num_points=NUMBER_OF_DATA_POINTS,
            models=models,
            metrics=metrics,
        )

        assert (
            len(data) == 12000
        )  # 3 models * 4 metrics * 1000 points each(NUMBER_OF_DATA_POINTS)
        assert data[0] == {"llm_id": 1, "metric_id": 1, "value": 3.5} # noqa
        mock_generate_random_value.assert_called()

    def test_generate_data_with_empty_models_or_metrics(self):
        data = generate_data(seed=42, num_points=2, models=[], metrics=[])
        assert data == []
