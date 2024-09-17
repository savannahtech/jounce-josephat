from abc import ABC, abstractmethod


class IUseCases(ABC):
    @abstractmethod
    def generate_llm_data(self):
        raise NotImplementedError

    @abstractmethod
    def fetch_metric_by_name(self, name):
        raise NotImplementedError

    @abstractmethod
    def fetch_metric_rankings_by_metric_id(self, metric_id):
        raise NotImplementedError

    @abstractmethod
    def rank_llms_by_metrics(self):
        raise NotImplementedError

    @abstractmethod
    def create_line_graph(self, data):
        raise NotImplementedError

    @abstractmethod
    def create_bar_graph(self, data):
        raise NotImplementedError
