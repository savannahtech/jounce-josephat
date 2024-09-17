from http import HTTPStatus

from flask import request
from flask_injector import inject
from marshmallow import Schema, fields

from src.application.ports.usecases import IUseCases
from src.infrastructure.utils.base import BaseAPIResource
from src.infrastructure.utils.helpers import api_key_authentication


class MessageResponseSchema(Schema):
    message = fields.String(required=True)
    kwargs = fields.Dict(required=False)


class LLMMetricsByName(BaseAPIResource):
    @inject
    def __init__(self, usecases: IUseCases):
        self.usecases = usecases

    method_decorators = [api_key_authentication] + BaseAPIResource.method_decorators # noqa

    def get(self):
        metric_name = request.args.get("metric_name")
        metric = self.usecases.fetch_metric_by_name(metric_name)
        if not metric:
            return {"detail": f"Invalid metric: {metric_name}"}, HTTPStatus.BAD_REQUEST # noqa

        results = self.usecases.fetch_metric_rankings_by_metric_id(metric.id)
        return {"results": results}, HTTPStatus.OK


class RankLLMMetricsAll(BaseAPIResource):
    @inject
    def __init__(self, usecases: IUseCases):
        self.usecases = usecases

    method_decorators = [api_key_authentication] + BaseAPIResource.method_decorators # noqa

    def get(self):
        results = self.usecases.rank_llms_by_metrics()
        return {"results": results}, HTTPStatus.OK


class HealthBase(BaseAPIResource):
    """This represents the applications health endpoint."""

    def get(self, **kwargs):
        return {"status": "healthy"}, HTTPStatus.OK
