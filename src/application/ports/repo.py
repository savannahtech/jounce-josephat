from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def bulk_create_record(self, values):
        raise NotImplementedError

    @abstractmethod
    def get_llm_metric_rankings_by_metric_id(self, metric):
        raise NotImplementedError

    @abstractmethod
    def get_all_llms(self):
        raise NotImplementedError

    @abstractmethod
    def get_metric_by_name(self, name):
        raise NotImplementedError

    @abstractmethod
    def get_all_metrics(self):
        raise NotImplementedError
