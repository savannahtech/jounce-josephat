import logging

import pytest

from src import create_app
from src.infrastructure.config.settings import TestConfig
from src.infrastructure.utils.extensions import db as _db
from tests.factories import LLMFactory, MetricFactory
from tests.settings import CustomTestApp


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app(TestConfig)
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def llm(db):
    data = [
        {"name": "GPT-4o"},
        {"name": "Mistral Large2"},
        {"name": "Llama 3.1 70B"},
    ]
    for dt in data:
        llm = LLMFactory(**dt)
        db.session.add(llm)
    db.session.commit()


@pytest.fixture
def metrics(db):
    metrics_data = [
        {
            "name": "TTFT",
            "description": "Time to First Token",
            "unit": "seconds",
            "min_value": 0.1,
            "max_value": 2.0,
        },
        {
            "name": "TPS",
            "description": "Tokens Per Second",
            "unit": "tokens/second",
            "min_value": 10,
            "max_value": 100,
        },
        {
            "name": "e2e_latency",
            "description": "End-to-End Request Latency",
            "unit": "seconds",
            "min_value": 0.5,
            "max_value": 5.0,
        },
        {
            "name": "RPS",
            "description": "Requests Per Second",
            "unit": "requests/second",
            "min_value": 1,
            "max_value": 50,
        },
    ]
    for metric_data in metrics_data:
        metric = MetricFactory(**metric_data)
        db.session.add(metric)
    db.session.commit()


@pytest.fixture
def testapp(app, db):
    yield CustomTestApp(app, db=db)
