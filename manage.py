from flask.cli import FlaskGroup

from app import app
from src.adapters.repositories.database import get_session
from src.application.domain.benchmark import LLM, Metric


cli = FlaskGroup(app)
session = get_session()


def initialize_metrics():
    metrics_data = [
        {"name": "TTFT", "description": "Time to First Token", "unit": "seconds", "min_value": 0.1, "max_value": 2.0},
        {"name": "TPS", "description": "Tokens Per Second", "unit": "tokens/second", "min_value": 10, "max_value": 100},
        {"name": "e2e_latency", "description": "End-to-End Request Latency", "unit": "seconds", "min_value": 0.5, "max_value": 5.0},
        {"name": "RPS", "description": "Requests Per Second", "unit": "requests/second", "min_value": 1, "max_value": 50}
    ]
    
    for metric_data in metrics_data:
        metric = session.query(Metric).filter_by(name=metric_data["name"]).first()
        if metric:
            metric.description = metric_data["description"]
            metric.unit = metric_data["unit"]
            metric.min_value = metric_data["min_value"]
            metric.max_value = metric_data["max_value"]
        else:
            metric = Metric(**metric_data)
            session.add(metric)
    
    session.commit()
    session.close()


def initialize_llms():
    llms_data = [
        {"name": "GPT-4o"},
        {"name": "Llama 3.1 405"},
        {"name": "Mistral Large2"},
        {"name": "Claude 3.5 Sonnet"},
        {"name": "Gemini 1.5 Pro"},
        {"name": "GPT-4o mini"},
        {"name": "Llama 3.1 70B"},
        {"name": "amba 1.5Large"},
        {"name": "Mixtral 8x22B"},
        {"name": "Gemini 1.5Flash"},
        {"name": "Claude 3 Haiku"},
        {"name": "Llama 3.1 8B"}
    ]
    
    for llm_data in llms_data:
        llm = session.query(LLM).filter_by(name=llm_data["name"]).first()
        if llm:
            print(f"llm {llm} already exists")
        else:
            llm = LLM(**llm_data)
            session.add(llm)
    
    session.commit()
    session.close()


@cli.command("initialize_metrics")
def init_metrics():
    initialize_metrics()
    print("Metrics initialized successfully.")


@cli.command("initialize_llms")
def init_llms():
    initialize_llms()
    print("LLMs initialized successfully.")


if __name__ == "__main__":
    cli()
