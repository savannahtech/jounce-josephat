import random
from functools import wraps
from typing import Dict, List

from flask import request

from src.application.domain.benchmark import Metric
from src.infrastructure.utils.exceptions import AuthenticationException
from src.infrastructure.utils.extensions import config


def validate_api_key(config_api_key, api_key, message):
    if not api_key:
        raise AuthenticationException(message)
    if api_key != config_api_key:
        raise AuthenticationException(message)


def handle_api_key_authentication(config_api_key):
    def authentication(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get("api-key")
            validate_api_key(config_api_key, api_key, "REQUEST-API-KEY-INVALID") # noqa
            return fn(*args, **kwargs)

        return wrapper

    return authentication


api_key_authentication = handle_api_key_authentication(config.get("API_KEY"))


def generate_random_value(metric_obj: Metric) -> float:
    """
    Generate a random value for a given metric based on predefined ranges.
    """
    if not metric_obj:
        raise ValueError("A valid Metric object must be provided")

    if metric_obj.min_value is None or metric_obj.max_value is None:
        raise ValueError(f"Metric {metric_obj.name} has no defined range.")

    return random.uniform(metric_obj.min_value, metric_obj.max_value)


def generate_data(
    seed: int, num_points: int, models: List[str], metrics: List[str]
) -> List[Dict[str, float]]:
    """
    Generate random benchmark data for a list of models and metrics.

    Args:
        seed (int): The random seed for reproducibility.
        num_points (int): Number of data points to generate per model and metric. # noqa
        models (List[str]): List of LLM models.
        metrics (List[str]): List of metrics.

    Returns:
        List[Dict[str, float]]: A list of dictionaries containing the benchmark results. # noqa
    """
    random.seed(seed)

    return [
        {
            "llm_id": model.id,
            "metric_id": metric.id,
            "value": generate_random_value(metric),
        }
        for model in models
        for metric in metrics
        for _ in range(num_points)
    ]
